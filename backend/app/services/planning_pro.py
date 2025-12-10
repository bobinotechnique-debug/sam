"""Planning PRO services for Phase 5 Step 03."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from app.core.logging import logger
from app.models.collaborator import Collaborator
from app.models.mission import Mission
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
from app.models.role import Role
from app.models.site import Site
from app.services.database import InMemoryDatabase
from app.services.errors import NotFoundError, ValidationError


def _overlaps(
    start_a: datetime, end_a: datetime, start_b: datetime, end_b: datetime
) -> bool:
    return start_a < end_b and start_b < end_a


class ShiftTemplateService:
    """Manage shift templates and derived instances."""

    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def list_templates(self, *, mission_id: int | None = None) -> list[ShiftTemplate]:
        templates = list(self._db.shift_templates.values())
        if mission_id is not None:
            templates = [t for t in templates if t.mission_id == mission_id]
        return templates

    def create_template(self, payload: ShiftTemplateCreate) -> ShiftTemplate:
        self._validate_references(
            mission_id=payload.mission_id,
            site_id=payload.site_id,
            role_id=payload.role_id,
        )
        template = ShiftTemplate(id=self._db.next_id("shift_templates"), **payload.model_dump())
        self._db.shift_templates[template.id] = template
        logger.info("Shift template created", extra={"template_id": template.id})
        return template

    def update_template(self, template_id: int, payload: ShiftTemplateUpdate) -> ShiftTemplate:
        existing = self._get_template(template_id)
        updates = payload.model_dump(exclude_none=True)
        mission_id = updates.get("mission_id", existing.mission_id)
        site_id = updates.get("site_id", existing.site_id)
        role_id = updates.get("role_id", existing.role_id)
        self._validate_references(mission_id=mission_id, site_id=site_id, role_id=role_id)
        updated = existing.model_copy(update=updates)
        self._db.shift_templates[template_id] = updated
        logger.info("Shift template updated", extra={"template_id": template_id})
        return updated

    def deactivate_template(self, template_id: int) -> None:
        template = self._get_template(template_id)
        updated = template.model_copy(update={"is_active": False})
        self._db.shift_templates[template_id] = updated
        logger.info("Shift template deactivated", extra={"template_id": template_id})

    def delete_template(self, template_id: int) -> None:
        self._get_template(template_id)
        self._db.shift_templates.pop(template_id, None)

    def _get_template(self, template_id: int) -> ShiftTemplate:
        template = self._db.shift_templates.get(template_id)
        if template is None:
            raise NotFoundError("Shift template not found")
        return template

    def _validate_references(self, *, mission_id: int, site_id: int, role_id: int) -> None:
        mission = self._db.missions.get(mission_id)
        site = self._db.sites.get(site_id)
        role = self._db.roles.get(role_id)
        if mission is None:
            raise NotFoundError("Mission not found")
        if site is None:
            raise NotFoundError("Site not found")
        if role is None:
            raise NotFoundError("Role not found")
        if mission.site_id != site_id or mission.role_id != role_id:
            raise ValidationError("Mission must match site and role references")


class ShiftInstanceService:
    """Manage concrete shift instances generated from templates or ad hoc."""

    def __init__(self, db: InMemoryDatabase, rule_service: RuleService) -> None:
        self._db = db
        self._rule_service = rule_service

    def list_instances(self, *, mission_id: int | None = None) -> list[ShiftWithAssignments]:
        instances = list(self._db.shift_instances.values())
        if mission_id is not None:
            instances = [i for i in instances if i.mission_id == mission_id]
        return [self._build_shift_view(instance) for instance in instances]

    def create_instance(self, payload: ShiftInstanceCreate) -> ShiftWithAssignments:
        mission = self._require_mission(payload.mission_id)
        self._require_site(payload.site_id)
        self._require_role(payload.role_id)
        if mission.site_id != payload.site_id or mission.role_id != payload.role_id:
            raise ValidationError("Shift must align with mission site and role")
        if payload.template_id is not None and payload.template_id not in self._db.shift_templates:
            raise NotFoundError("Shift template not found")
        instance = ShiftInstance(id=self._db.next_id("shift_instances"), **payload.model_dump())
        self._db.shift_instances[instance.id] = instance
        conflicts = self._rule_service.evaluate_shift(instance)
        logger.info("Shift instance created", extra={"shift_instance_id": instance.id})
        return ShiftWithAssignments(shift=instance, assignments=[], conflicts=conflicts)

    def update_instance(
        self, instance_id: int, payload: ShiftInstanceUpdate
    ) -> ShiftWithAssignments:
        existing = self._get_instance(instance_id)
        updates = payload.model_dump(exclude_none=True)
        mission_id = updates.get("mission_id", existing.mission_id)
        site_id = updates.get("site_id", existing.site_id)
        role_id = updates.get("role_id", existing.role_id)
        mission = self._require_mission(mission_id)
        self._require_site(site_id)
        self._require_role(role_id)
        if mission.site_id != site_id or mission.role_id != role_id:
            raise ValidationError("Shift must align with mission site and role")
        updated = existing.model_copy(update=updates)
        self._db.shift_instances[instance_id] = updated
        conflicts = self._rule_service.evaluate_shift(updated)
        assignments = [
            a for a in self._db.assignments.values() if a.shift_instance_id == instance_id
        ]
        return ShiftWithAssignments(
            shift=updated, assignments=assignments, conflicts=conflicts
        )

    def delete_instance(self, instance_id: int) -> None:
        self._get_instance(instance_id)
        for assignment_id, assignment in list(self._db.assignments.items()):
            if assignment.shift_instance_id == instance_id:
                self._db.assignments.pop(assignment_id, None)
        self._db.shift_instances.pop(instance_id, None)

    def _get_instance(self, instance_id: int) -> ShiftInstance:
        instance = self._db.shift_instances.get(instance_id)
        if instance is None:
            raise NotFoundError("Shift instance not found")
        return instance

    def _build_shift_view(self, instance: ShiftInstance) -> ShiftWithAssignments:
        assignments = [
            a for a in self._db.assignments.values() if a.shift_instance_id == instance.id
        ]
        conflicts = self._rule_service.evaluate_shift(instance)
        for assignment in assignments:
            conflicts.extend(self._rule_service.evaluate_assignment(assignment))
        return ShiftWithAssignments(shift=instance, assignments=assignments, conflicts=conflicts)

    def _require_mission(self, mission_id: int) -> Mission:
        mission = self._db.missions.get(mission_id)
        if mission is None:
            raise NotFoundError("Mission not found")
        return mission

    def _require_site(self, site_id: int) -> Site:
        site = self._db.sites.get(site_id)
        if site is None:
            raise NotFoundError("Site not found")
        return site

    def _require_role(self, role_id: int) -> Role:
        role = self._db.roles.get(role_id)
        if role is None:
            raise NotFoundError("Role not found")
        return role


class AssignmentService:
    """Handle collaborator assignments on shift instances."""

    def __init__(self, db: InMemoryDatabase, rule_service: RuleService) -> None:
        self._db = db
        self._rule_service = rule_service

    def list_assignments(self, *, instance_id: int | None = None) -> list[Assignment]:
        assignments = list(self._db.assignments.values())
        if instance_id is not None:
            assignments = [a for a in assignments if a.shift_instance_id == instance_id]
        return assignments

    def create_assignment(
        self, payload: AssignmentCreate
    ) -> tuple[Assignment, list[ConflictEntry]]:
        shift = self._require_shift(payload.shift_instance_id)
        self._require_collaborator(payload.collaborator_id)
        if shift.status == "cancelled":
            raise ValidationError("Cannot assign to a cancelled shift")
        if payload.role_id != shift.role_id:
            raise ValidationError("Assignment role must match shift role")
        assignment = Assignment(
            id=self._db.next_id("assignments"), **payload.model_dump()
        )
        self._db.assignments[assignment.id] = assignment
        conflicts = self._rule_service.evaluate_assignment(assignment, shift=shift)
        logger.info("Assignment created", extra={"assignment_id": assignment.id})
        return assignment, conflicts

    def update_assignment(
        self, assignment_id: int, payload: AssignmentUpdate
    ) -> tuple[Assignment, list[ConflictEntry]]:
        existing = self._get_assignment(assignment_id)
        updates = payload.model_dump(exclude_none=True)
        shift = self._require_shift(
            updates.get("shift_instance_id", existing.shift_instance_id)
        )
        self._require_collaborator(
            updates.get("collaborator_id", existing.collaborator_id)
        )
        if shift.status == "cancelled":
            raise ValidationError("Cannot assign to a cancelled shift")
        if updates.get("role_id", existing.role_id) != shift.role_id:
            raise ValidationError("Assignment role must match shift role")
        updated = existing.model_copy(update=updates)
        self._db.assignments[assignment_id] = updated
        conflicts = self._rule_service.evaluate_assignment(updated, shift=shift)
        return updated, conflicts

    def delete_assignment(self, assignment_id: int) -> None:
        self._get_assignment(assignment_id)
        self._db.assignments.pop(assignment_id, None)

    def bulk_upsert(self, payloads: Iterable[AssignmentCreate]) -> list[Assignment]:
        created: list[Assignment] = []
        for payload in payloads:
            assignment, _ = self.create_assignment(payload)
            created.append(assignment)
        return created

    def lock(self, assignment_id: int, *, locked: bool) -> Assignment:
        assignment = self._get_assignment(assignment_id)
        updated = assignment.model_copy(update={"is_locked": locked})
        self._db.assignments[assignment_id] = updated
        return updated

    def _require_shift(self, shift_id: int) -> ShiftInstance:
        shift = self._db.shift_instances.get(shift_id)
        if shift is None:
            raise NotFoundError("Shift not found")
        return shift

    def _require_collaborator(self, collaborator_id: int) -> Collaborator:
        collaborator = self._db.collaborators.get(collaborator_id)
        if collaborator is None:
            raise NotFoundError("Collaborator not found")
        return collaborator

    def _get_assignment(self, assignment_id: int) -> Assignment:
        assignment = self._db.assignments.get(assignment_id)
        if assignment is None:
            raise NotFoundError("Assignment not found")
        return assignment


class AvailabilityService:
    """Track user availability, leaves and blackout overlays."""

    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def record_availability(self, payload: UserAvailabilityCreate) -> UserAvailability:
        availability = UserAvailability(
            id=self._db.next_id("user_availabilities"), **payload.model_dump()
        )
        self._db.user_availabilities[availability.id] = availability
        return availability

    def list_availability(self, *, collaborator_id: int | None = None) -> list[UserAvailability]:
        availabilities = list(self._db.user_availabilities.values())
        if collaborator_id is not None:
            availabilities = [a for a in availabilities if a.collaborator_id == collaborator_id]
        return availabilities

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
    """Evaluate HR and conflict rules for planning validation."""

    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db
        if not self._db.conflict_rules:
            self._seed_rules()

    def list_hr_rules(self, organization_id: int) -> list[HrRule]:
        return [
            rule
            for rule in self._db.hr_rules.values()
            if rule.organization_id == organization_id
        ]

    def list_conflict_rules(self, organization_id: int) -> list[ConflictRule]:
        return [
            rule
            for rule in self._db.conflict_rules.values()
            if rule.organization_id == organization_id
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
        shift_instance = shift or self._db.shift_instances.get(assignment.shift_instance_id)
        if shift_instance is None:
            return conflicts
        # Double booking detection
        for other in self._db.assignments.values():
            if getattr(other, "id", None) == getattr(assignment, "id", None):
                continue
            if other.collaborator_id != assignment.collaborator_id:
                continue
            other_shift = self._db.shift_instances.get(other.shift_instance_id)
            if other_shift is None or other_shift.status == "cancelled":
                continue
            if _overlaps(
                shift_instance.start_utc,
                shift_instance.end_utc,
                other_shift.start_utc,
                other_shift.end_utc,
            ):
                conflicts.append(
                    ConflictEntry(
                        type="hard",
                        rule="double_booking",
                        details={"other_shift_id": other_shift.id},
                    )
                )
        # Minimum rest check (1 hour)
        by_collaborator = [
            other
            for other in self._db.assignments.values()
            if other.collaborator_id == assignment.collaborator_id
            and getattr(other, "id", None) != getattr(assignment, "id", None)
        ]
        for other in by_collaborator:
            other_shift = self._db.shift_instances.get(other.shift_instance_id)
            if other_shift is None:
                continue
            rest_gap = (shift_instance.start_utc - other_shift.end_utc).total_seconds()
            if 0 < rest_gap < 3600:
                conflicts.append(
                    ConflictEntry(
                        type="hard",
                        rule="rest_gap",
                        details={"previous_shift_id": other_shift.id},
                    )
                )
        # Availability / leave
        for availability in self._db.user_availabilities.values():
            if availability.collaborator_id != assignment.collaborator_id:
                continue
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
        # Simple defaults for preview purposes
        org_id = 1
        hr_rule = HrRule(
            id=self._db.next_id("hr_rules"),
            organization_id=org_id,
            code="rest_minimum",
            severity="hard",
            description="Minimum 1 hour rest between shifts",
            config={"hours": 1},
        )
        conflict_rule = ConflictRule(
            id=self._db.next_id("conflict_rules"),
            organization_id=org_id,
            code="double_booking",
            severity="error",
            description="Collaborator cannot be assigned to overlapping shifts",
            config={"enforced": True},
        )
        self._db.hr_rules[hr_rule.id] = hr_rule
        self._db.conflict_rules[conflict_rule.id] = conflict_rule


class AuditService:
    """Log planning changes for auditability."""

    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

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
        entry = {
            "organization_id": organization_id,
            "actor_user_id": actor_user_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": action,
            "payload": payload,
            "timestamp": datetime.now(UTC),
        }
        self._db.planning_changes.append(entry)
        logger.info(
            "Planning change logged",
            extra={"entity_type": entity_type, "entity_id": entity_id},
        )

    def list_changes(self) -> list[dict[str, Any]]:
        return list(self._db.planning_changes)


class PublicationService:
    """Create and publish planning snapshots."""

    def __init__(self, db: InMemoryDatabase, audit_service: AuditService) -> None:
        self._db = db
        self._audit_service = audit_service

    def prepare_draft(self, organization_id: int, message: str | None = None) -> Publication:
        publication = Publication(
            id=self._db.next_id("publications"),
            organization_id=organization_id,
            message=message,
            status="draft",
            version=1,
            published_at=None,
        )
        self._db.publications[publication.id] = publication
        return publication

    def publish(self, publication_id: int) -> Publication:
        publication = self._db.publications.get(publication_id)
        if publication is None:
            raise NotFoundError("Publication not found")
        updated = publication.model_copy(
            update={"status": "published", "published_at": datetime.now(UTC)}
        )
        self._db.publications[publication_id] = updated
        self._audit_service.log_change(
            organization_id=publication.organization_id,
            actor_user_id=None,
            entity_type="publication",
            entity_id=publication_id,
            action="publish_planning",
            payload={"publication_id": publication_id},
        )
        return updated

    def list_events(self, organization_id: int) -> list[NotificationEvent]:
        return [
            event
            for event in self._db.notification_events.values()
            if event.organization_id == organization_id
        ]


class AutoAssignJobService:
    def __init__(
        self, db: InMemoryDatabase, assignment_service: AssignmentService
    ) -> None:
        self._db = db
        self._assignment_service = assignment_service

    def start_job(self, *, shift_ids: list[int] | None = None) -> dict[str, Any]:
        job_id = f"job-{self._db.next_id('auto_assign_jobs')}"
        created_assignments = []
        targets = (
            [
                self._db.shift_instances[sid]
                for sid in shift_ids or []
                if sid in self._db.shift_instances
            ]
            if shift_ids
            else list(self._db.shift_instances.values())
        )
        for shift in targets:
            if any(
                a.shift_instance_id == shift.id
                for a in self._db.assignments.values()
            ):
                continue
            collaborator_ids = list(self._db.collaborators.keys())
            if not collaborator_ids:
                continue
            collaborator_id = collaborator_ids[0]
            assignment_payload = AssignmentCreate(
                shift_instance_id=shift.id,
                collaborator_id=collaborator_id,
                role_id=shift.role_id,
                status="proposed",
                source="auto-assign-v1",
            )
            assignment, conflicts = self._assignment_service.create_assignment(
                assignment_payload
            )
            created_assignments.append({
                "assignment": assignment,
                "conflicts": conflicts,
            })
        job_payload = {
            "job_id": job_id,
            "status": "completed",
            "assignments_created": len(created_assignments),
            "conflicts": [
                conflict
                for item in created_assignments
                for conflict in item["conflicts"]
            ],
        }
        self._db.auto_assign_jobs[job_id] = job_payload
        return job_payload

    def get_status(self, job_id: str) -> dict[str, Any]:
        job = self._db.auto_assign_jobs.get(job_id)
        if job is None:
            raise NotFoundError("Job not found")
        return job
