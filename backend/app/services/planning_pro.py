from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logging import logger
from app.db.models import planning as db_models
from app.models.planning_pro import (
    Assignment,
    AssignmentCreate,
    AssignmentUpdate,
    ConflictEntry,
    ConflictRule,
    HrRule,
    NotificationEvent,
    Publication,
    ShiftInstance,
    ShiftInstanceCreate,
    ShiftInstanceUpdate,
    ShiftTemplate,
    ShiftTemplateCreate,
    ShiftTemplateUpdate,
    ShiftWithAssignments,
    UserAvailability,
    UserAvailabilityCreate,
)
from app.services.errors import NotFoundError, ValidationError


def _overlaps(
    start_a: datetime, end_a: datetime, start_b: datetime, end_b: datetime
) -> bool:
    return start_a < end_b and start_b < end_a


def _ensure_timezone(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


def _to_shift_template(model: db_models.ShiftTemplate) -> ShiftTemplate:
    return ShiftTemplate(
        id=model.id,
        mission_id=model.mission_id,
        site_id=model.site_id,
        role_id=model.role_id,
        team_id=model.team_id,
        recurrence_rule=model.recurrence_rule,
        start_time_utc=_ensure_timezone(model.start_time_utc),
        end_time_utc=_ensure_timezone(model.end_time_utc),
        expected_headcount=model.expected_headcount,
        is_active=model.is_active,
    )


def _to_shift_instance(model: db_models.ShiftInstance) -> ShiftInstance:
    return ShiftInstance(
        id=model.id,
        mission_id=model.mission_id,
        template_id=model.template_id,
        site_id=model.site_id,
        role_id=model.role_id,
        team_id=model.team_id,
        start_utc=_ensure_timezone(model.start_utc),
        end_utc=_ensure_timezone(model.end_utc),
        status=model.status,
        source=model.source,
        capacity=model.capacity,
    )


def _to_assignment(model: db_models.Assignment) -> Assignment:
    return Assignment(
        id=model.id,
        shift_instance_id=model.shift_instance_id,
        collaborator_id=model.collaborator_id,
        role_id=model.role_id,
        status=model.status,
        source=model.source,
        note=model.note,
        is_locked=model.is_locked,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_availability(model: db_models.UserAvailability) -> UserAvailability:
    return UserAvailability(
        id=model.id,
        collaborator_id=model.collaborator_id,
        start_utc=model.start_utc,
        end_utc=model.end_utc,
        is_available=model.is_available,
        reason=model.reason,
    )


def _to_publication(model: db_models.Publication) -> Publication:
    return Publication(
        id=model.id,
        organization_id=model.organization_id,
        author_user_id=model.author_user_id,
        status=model.status,
        version=model.version,
        message=model.message,
        published_at=model.published_at,
    )


class ShiftTemplateService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_templates(self, *, mission_id: int | None = None) -> list[ShiftTemplate]:
        query = select(db_models.ShiftTemplate)
        if mission_id is not None:
            query = query.where(db_models.ShiftTemplate.mission_id == mission_id)
        templates = self._session.scalars(query).all()
        return [_to_shift_template(template) for template in templates]

    def create_template(self, payload: ShiftTemplateCreate) -> ShiftTemplate:
        self._validate_references(
            mission_id=payload.mission_id,
            site_id=payload.site_id,
            role_id=payload.role_id,
        )
        template = db_models.ShiftTemplate(**payload.model_dump())
        self._session.add(template)
        self._session.commit()
        self._session.refresh(template)
        logger.info("Shift template created", extra={"template_id": template.id})
        return _to_shift_template(template)

    def update_template(self, template_id: int, payload: ShiftTemplateUpdate) -> ShiftTemplate:
        template = self._get_template(template_id)
        updates = payload.model_dump(exclude_none=True)
        mission_id = updates.get("mission_id", template.mission_id)
        site_id = updates.get("site_id", template.site_id)
        role_id = updates.get("role_id", template.role_id)
        self._validate_references(mission_id=mission_id, site_id=site_id, role_id=role_id)
        for field, value in updates.items():
            setattr(template, field, value)
        self._session.commit()
        self._session.refresh(template)
        logger.info("Shift template updated", extra={"template_id": template_id})
        return _to_shift_template(template)

    def deactivate_template(self, template_id: int) -> None:
        template = self._get_template(template_id)
        template.is_active = False
        self._session.commit()

    def delete_template(self, template_id: int) -> None:
        template = self._get_template(template_id)
        self._session.delete(template)
        self._session.commit()

    def _get_template(self, template_id: int) -> db_models.ShiftTemplate:
        template = self._session.get(db_models.ShiftTemplate, template_id)
        if template is None:
            raise NotFoundError("Shift template not found")
        return template

    def _validate_references(self, *, mission_id: int, site_id: int, role_id: int) -> None:
        mission = self._session.get(db_models.Mission, mission_id)
        site = self._session.get(db_models.Site, site_id)
        role = self._session.get(db_models.Role, role_id)
        if mission is None:
            raise NotFoundError("Mission not found")
        if site is None:
            raise NotFoundError("Site not found")
        if role is None:
            raise NotFoundError("Role not found")
        if mission.site_id != site_id or mission.role_id != role_id:
            raise ValidationError("Mission must match site and role references")


class ShiftInstanceService:
    def __init__(self, session: Session, rule_service: RuleService) -> None:
        self._session = session
        self._rule_service = rule_service

    def list_instances(self, *, mission_id: int | None = None) -> list[ShiftWithAssignments]:
        query = select(db_models.ShiftInstance)
        if mission_id is not None:
            query = query.where(db_models.ShiftInstance.mission_id == mission_id)
        instances = self._session.scalars(query).all()
        return [self._build_shift_view(instance) for instance in instances]

    def create_instance(self, payload: ShiftInstanceCreate) -> ShiftWithAssignments:
        mission = self._require_mission(payload.mission_id)
        self._require_site(payload.site_id)
        self._require_role(payload.role_id)
        if mission.site_id != payload.site_id or mission.role_id != payload.role_id:
            raise ValidationError("Shift must align with mission site and role")
        if payload.template_id is not None and self._session.get(
            db_models.ShiftTemplate, payload.template_id
        ) is None:
            raise NotFoundError("Shift template not found")
        instance = db_models.ShiftInstance(**payload.model_dump())
        self._session.add(instance)
        self._session.commit()
        self._session.refresh(instance)
        conflicts = self._rule_service.evaluate_shift(_to_shift_instance(instance))
        logger.info("Shift instance created", extra={"shift_instance_id": instance.id})
        return ShiftWithAssignments(
            shift=_to_shift_instance(instance),
            assignments=[],
            conflicts=conflicts,
        )

    def update_instance(
        self, instance_id: int, payload: ShiftInstanceUpdate
    ) -> ShiftWithAssignments:
        instance = self._get_instance(instance_id)
        updates = payload.model_dump(exclude_none=True)
        mission_id = updates.get("mission_id", instance.mission_id)
        site_id = updates.get("site_id", instance.site_id)
        role_id = updates.get("role_id", instance.role_id)
        mission = self._require_mission(mission_id)
        self._require_site(site_id)
        self._require_role(role_id)
        if mission.site_id != site_id or mission.role_id != role_id:
            raise ValidationError("Shift must align with mission site and role")
        for field, value in updates.items():
            setattr(instance, field, value)
        self._session.commit()
        self._session.refresh(instance)
        conflicts = self._rule_service.evaluate_shift(_to_shift_instance(instance))
        assignments = self._session.scalars(
            select(db_models.Assignment).where(
                db_models.Assignment.shift_instance_id == instance_id
            )
        ).all()
        return ShiftWithAssignments(
            shift=_to_shift_instance(instance),
            assignments=[_to_assignment(a) for a in assignments],
            conflicts=conflicts,
        )

    def delete_instance(self, instance_id: int) -> None:
        instance = self._get_instance(instance_id)
        self._session.query(db_models.Assignment).filter(
            db_models.Assignment.shift_instance_id == instance_id
        ).delete()
        self._session.delete(instance)
        self._session.commit()

    def _get_instance(self, instance_id: int) -> db_models.ShiftInstance:
        instance = self._session.get(db_models.ShiftInstance, instance_id)
        if instance is None:
            raise NotFoundError("Shift instance not found")
        return instance

    def _build_shift_view(self, instance: db_models.ShiftInstance) -> ShiftWithAssignments:
        assignments = self._session.scalars(
            select(db_models.Assignment).where(
                db_models.Assignment.shift_instance_id == instance.id
            )
        ).all()
        shift = _to_shift_instance(instance)
        conflicts = self._rule_service.evaluate_shift(shift)
        for assignment in assignments:
            conflicts.extend(
                self._rule_service.evaluate_assignment(_to_assignment(assignment), shift=shift)
            )
        return ShiftWithAssignments(
            shift=shift,
            assignments=[_to_assignment(a) for a in assignments],
            conflicts=conflicts,
        )

    def _require_mission(self, mission_id: int) -> db_models.Mission:
        mission = self._session.get(db_models.Mission, mission_id)
        if mission is None:
            raise NotFoundError("Mission not found")
        return mission

    def _require_site(self, site_id: int) -> db_models.Site:
        site = self._session.get(db_models.Site, site_id)
        if site is None:
            raise NotFoundError("Site not found")
        return site

    def _require_role(self, role_id: int) -> db_models.Role:
        role = self._session.get(db_models.Role, role_id)
        if role is None:
            raise NotFoundError("Role not found")
        return role


class AssignmentService:
    def __init__(self, session: Session, rule_service: RuleService) -> None:
        self._session = session
        self._rule_service = rule_service

    def list_assignments(self, *, instance_id: int | None = None) -> list[Assignment]:
        query = select(db_models.Assignment)
        if instance_id is not None:
            query = query.where(db_models.Assignment.shift_instance_id == instance_id)
        assignments = self._session.scalars(query).all()
        return [_to_assignment(a) for a in assignments]

    def create_assignment(
        self, payload: AssignmentCreate
    ) -> tuple[Assignment, list[ConflictEntry]]:
        shift = self._require_shift(payload.shift_instance_id)
        self._require_collaborator(payload.collaborator_id)
        if shift.status == "cancelled":
            raise ValidationError("Cannot assign to a cancelled shift")
        if payload.role_id != shift.role_id:
            raise ValidationError("Assignment role must match shift role")
        assignment = db_models.Assignment(**payload.model_dump())
        self._session.add(assignment)
        self._session.commit()
        self._session.refresh(assignment)
        conflicts = self._rule_service.evaluate_assignment(
            _to_assignment(assignment), shift=_to_shift_instance(shift)
        )
        logger.info("Assignment created", extra={"assignment_id": assignment.id})
        return _to_assignment(assignment), conflicts

    def update_assignment(
        self, assignment_id: int, payload: AssignmentUpdate
    ) -> tuple[Assignment, list[ConflictEntry]]:
        assignment = self._get_assignment(assignment_id)
        updates = payload.model_dump(exclude_none=True)
        shift = self._require_shift(updates.get("shift_instance_id", assignment.shift_instance_id))
        self._require_collaborator(updates.get("collaborator_id", assignment.collaborator_id))
        if shift.status == "cancelled":
            raise ValidationError("Cannot assign to a cancelled shift")
        if updates.get("role_id", assignment.role_id) != shift.role_id:
            raise ValidationError("Assignment role must match shift role")
        for field, value in updates.items():
            setattr(assignment, field, value)
        self._session.commit()
        self._session.refresh(assignment)
        conflicts = self._rule_service.evaluate_assignment(
            _to_assignment(assignment), shift=_to_shift_instance(shift)
        )
        return _to_assignment(assignment), conflicts

    def delete_assignment(self, assignment_id: int) -> None:
        assignment = self._get_assignment(assignment_id)
        self._session.delete(assignment)
        self._session.commit()

    def bulk_upsert(self, payloads: Iterable[AssignmentCreate]) -> list[Assignment]:
        created: list[Assignment] = []
        for payload in payloads:
            assignment, _ = self.create_assignment(payload)
            created.append(assignment)
        return created

    def lock(self, assignment_id: int, *, locked: bool) -> Assignment:
        assignment = self._get_assignment(assignment_id)
        assignment.is_locked = locked
        self._session.commit()
        self._session.refresh(assignment)
        return _to_assignment(assignment)

    def _require_shift(self, shift_id: int) -> db_models.ShiftInstance:
        shift = self._session.get(db_models.ShiftInstance, shift_id)
        if shift is None:
            raise NotFoundError("Shift not found")
        return shift

    def _require_collaborator(self, collaborator_id: int) -> db_models.Collaborator:
        collaborator = self._session.get(db_models.Collaborator, collaborator_id)
        if collaborator is None:
            raise NotFoundError("Collaborator not found")
        return collaborator

    def _get_assignment(self, assignment_id: int) -> db_models.Assignment:
        assignment = self._session.get(db_models.Assignment, assignment_id)
        if assignment is None:
            raise NotFoundError("Assignment not found")
        return assignment


class AvailabilityService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def record_availability(self, payload: UserAvailabilityCreate) -> UserAvailability:
        availability = db_models.UserAvailability(**payload.model_dump())
        self._session.add(availability)
        self._session.commit()
        self._session.refresh(availability)
        return _to_availability(availability)

    def list_availability(self, *, collaborator_id: int | None = None) -> list[UserAvailability]:
        query = select(db_models.UserAvailability)
        if collaborator_id is not None:
            query = query.where(db_models.UserAvailability.collaborator_id == collaborator_id)
        availabilities = self._session.scalars(query).all()
        return [_to_availability(a) for a in availabilities]

    def record_leave(
        self, *, collaborator_id: int, start: datetime, end: datetime, category: str
    ) -> None:
        self.record_availability(
            UserAvailabilityCreate(
                collaborator_id=collaborator_id,
                start_utc=start,
                end_utc=end,
                is_available=False,
                reason=category,
            )
        )


class RuleService:
    def __init__(self, session: Session) -> None:
        self._session = session
        if not self._session.scalar(select(db_models.ConflictRule.id)):
            self._seed_rules()

    def list_hr_rules(self, organization_id: int) -> list[HrRule]:
        rules = self._session.scalars(
            select(db_models.HrRule).where(db_models.HrRule.organization_id == organization_id)
        ).all()
        return [
            HrRule(
                id=rule.id,
                organization_id=rule.organization_id,
                code=rule.code,
                severity=rule.severity,
                description=rule.description,
                config=rule.config,
            )
            for rule in rules
        ]

    def list_conflict_rules(self, organization_id: int) -> list[ConflictRule]:
        rules = self._session.scalars(
            select(db_models.ConflictRule).where(
                db_models.ConflictRule.organization_id == organization_id
            )
        ).all()
        return [
            ConflictRule(
                id=rule.id,
                organization_id=rule.organization_id,
                code=rule.code,
                severity=rule.severity,
                description=rule.description,
                config=rule.config,
            )
            for rule in rules
        ]

    def evaluate_instance(self, instance: ShiftInstance) -> list[str]:
        conflicts = self.evaluate_shift(instance)
        return [conflict.rule for conflict in conflicts]

    def evaluate_shift(self, instance: ShiftInstance | ShiftInstanceCreate) -> list[ConflictEntry]:
        conflicts: list[ConflictEntry] = []
        if instance.start_utc >= instance.end_utc:
            conflicts.append(
                ConflictEntry(
                    type="hard",
                    rule="time_order",
                    details={"message": "start must be before end"},
                )
            )
        if instance.status not in {"draft", "published", "cancelled"}:
            conflicts.append(
                ConflictEntry(
                    type="hard",
                    rule="invalid_status",
                    details={"status": instance.status},
                )
            )
        return conflicts

    def evaluate_assignment(
        self, assignment: Assignment | AssignmentCreate, shift: ShiftInstance | None = None
    ) -> list[ConflictEntry]:
        conflicts: list[ConflictEntry] = []
        db_shift = self._session.get(db_models.ShiftInstance, assignment.shift_instance_id)
        shift_instance = shift or (_to_shift_instance(db_shift) if db_shift else None)
        if shift_instance is None:
            return conflicts
        for other in self._session.scalars(select(db_models.Assignment)).all():
            if getattr(other, "id", None) == getattr(assignment, "id", None):
                continue
            if other.collaborator_id != assignment.collaborator_id:
                continue
            other_shift = self._session.get(db_models.ShiftInstance, other.shift_instance_id)
            if other_shift is None or other_shift.status == "cancelled":
                continue
            if _overlaps(
                shift_instance.start_utc,
                shift_instance.end_utc,
                _ensure_timezone(other_shift.start_utc),
                _ensure_timezone(other_shift.end_utc),
            ):
                conflicts.append(
                    ConflictEntry(
                        type="hard",
                        rule="double_booking",
                        details={"other_shift_id": other_shift.id},
                    )
                )
        availabilities = self._session.scalars(
            select(db_models.UserAvailability).where(
                db_models.UserAvailability.collaborator_id == assignment.collaborator_id
            )
        ).all()
        for availability in availabilities:
            if _overlaps(
                shift_instance.start_utc,
                shift_instance.end_utc,
                availability.start_utc,
                availability.end_utc,
            ):
                if not availability.is_available:
                    conflicts.append(
                        ConflictEntry(
                            type="hard",
                            rule="leave",
                            details={"reason": availability.reason},
                        )
                    )
                else:
                    conflicts.append(
                        ConflictEntry(
                            type="soft",
                            rule="availability_partial",
                            details={"reason": availability.reason},
                        )
                    )
        return conflicts

    def _seed_rules(self) -> None:
        org_id = 1
        hr_rule = db_models.HrRule(
            organization_id=org_id,
            code="rest_minimum",
            severity="hard",
            description="Minimum rest between shifts",
            config={"hours": 1},
        )
        conflict_rule = db_models.ConflictRule(
            organization_id=org_id,
            code="double_booking",
            severity="error",
            description="Collaborator cannot be assigned to overlapping shifts",
            config={"enforced": True},
        )
        self._session.add_all([hr_rule, conflict_rule])
        self._session.commit()


class AuditService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def log_change(
        self,
        *,
        organization_id: int,
        actor_user_id: int | None,
        entity_type: str,
        entity_id: int,
        action: str,
        payload: dict[str, Any],
    ) -> None:
        entry = db_models.PlanningChange(
            organization_id=organization_id,
            actor_user_id=actor_user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            payload=jsonable_encoder(payload),
        )
        self._session.add(entry)
        self._session.commit()
        logger.info(
            "Planning change logged",
            extra={"entity_type": entity_type, "entity_id": entity_id},
        )

    def list_changes(self) -> list[dict[str, Any]]:
        changes = self._session.scalars(select(db_models.PlanningChange)).all()
        return [
            {
                "organization_id": change.organization_id,
                "actor_user_id": change.actor_user_id,
                "entity_type": change.entity_type,
                "entity_id": change.entity_id,
                "action": change.action,
                "payload": change.payload,
                "timestamp": change.created_at,
            }
            for change in changes
        ]


class PublicationService:
    def __init__(self, session: Session, audit_service: AuditService) -> None:
        self._session = session
        self._audit_service = audit_service

    def prepare_draft(self, organization_id: int, message: str | None = None) -> Publication:
        publication = db_models.Publication(
            organization_id=organization_id,
            message=message,
            status="draft",
            version=1,
            published_at=None,
        )
        self._session.add(publication)
        self._session.commit()
        self._session.refresh(publication)
        return _to_publication(publication)

    def publish(self, publication_id: int) -> Publication:
        publication = self._session.get(db_models.Publication, publication_id)
        if publication is None:
            raise NotFoundError("Publication not found")
        publication.status = "published"
        publication.published_at = datetime.now(UTC)
        self._session.commit()
        self._session.refresh(publication)
        self._audit_service.log_change(
            organization_id=publication.organization_id,
            actor_user_id=None,
            entity_type="publication",
            entity_id=publication_id,
            action="publish_planning",
            payload={"publication_id": publication_id},
        )
        return _to_publication(publication)

    def list_events(self, organization_id: int) -> list[NotificationEvent]:
        events = self._session.scalars(
            select(db_models.NotificationEvent).where(
                db_models.NotificationEvent.organization_id == organization_id
            )
        ).all()
        return [
            NotificationEvent(
                id=event.id,
                organization_id=event.organization_id,
                recipient_user_id=event.recipient_user_id,
                event_type=event.event_type,
                payload=event.payload,
                related_shift_instance_id=event.related_shift_instance_id,
                created_at=event.created_at,
                read_at=event.read_at,
            )
            for event in events
        ]


class AutoAssignJobService:
    def __init__(
        self, session: Session, assignment_service: AssignmentService
    ) -> None:
        self._session = session
        self._assignment_service = assignment_service
        self._jobs: dict[str, dict[str, Any]] = {}

    def start_job(self, *, shift_ids: list[int] | None = None) -> dict[str, Any]:
        job_id = f"job-{int(datetime.now(UTC).timestamp())}"
        created_assignments: list[dict[str, Any]] = []
        targets = (
            self._session.scalars(
                select(db_models.ShiftInstance).where(db_models.ShiftInstance.id.in_(shift_ids))
            ).all()
            if shift_ids
            else self._session.scalars(select(db_models.ShiftInstance)).all()
        )
        for shift in targets:
            if self._session.scalar(
                select(db_models.Assignment.id).where(
                    db_models.Assignment.shift_instance_id == shift.id
                )
            ):
                continue
            collaborator_id = self._session.scalar(select(db_models.Collaborator.id))
            if collaborator_id is None:
                continue
            assignment_payload = AssignmentCreate(
                shift_instance_id=shift.id,
                collaborator_id=collaborator_id,
                role_id=shift.role_id,
                status="proposed",
                source="auto-assign-v1",
            )
            assignment, conflicts = self._assignment_service.create_assignment(assignment_payload)
            created_assignments.append({"assignment": assignment, "conflicts": conflicts})
        job_payload: dict[str, Any] = {
            "job_id": job_id,
            "status": "completed",
            "assignments_created": len(created_assignments),
            "conflicts": [
                conflict for item in created_assignments for conflict in item["conflicts"]
            ],
        }
        self._jobs[job_id] = job_payload
        return job_payload

    def get_status(self, job_id: str) -> dict[str, Any]:
        job = self._jobs.get(job_id)
        if job is None:
            raise NotFoundError("Job not found")
        return job
