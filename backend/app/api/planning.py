from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.models.planning_pro import (
    Assignment,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentWriteResponse,
    ConflictEntry,
    ConflictRule,
    HrRule,
    Publication,
    ShiftInstance,
    ShiftInstanceCreate,
    ShiftInstanceUpdate,
    ShiftTemplate,
    ShiftTemplateCreate,
    ShiftTemplateUpdate,
    ShiftWithAssignments,
    ShiftWriteResponse,
    UserAvailability,
    UserAvailabilityCreate,
)
from app.services.planning_pro import (
    AssignmentService,
    AuditService,
    AutoAssignJobService,
    AvailabilityService,
    PublicationService,
    RuleService,
    ShiftInstanceService,
    ShiftTemplateService,
)

router = APIRouter(prefix="/api/v1/planning", tags=["planning_pro"])


class ConflictPreviewPayload(BaseModel):
    shift: ShiftInstanceCreate | None = None
    assignments: list[AssignmentCreate] | None = None


class PublishRequest(BaseModel):
    message: str | None = None


class ConflictPreviewResult(BaseModel):
    shift: ShiftInstanceCreate | ShiftInstance | None = None
    assignment: AssignmentCreate | Assignment | None = None
    conflicts: list[ConflictEntry]


class AutoAssignStartRequest(BaseModel):
    shift_ids: list[int] | None = None


SessionDep = Annotated[Session, Depends(get_session)]


def get_planning_services(session: SessionDep) -> dict[str, object]:
    rule_service = RuleService(session)
    template_service = ShiftTemplateService(session)
    instance_service = ShiftInstanceService(session, rule_service)
    assignment_service = AssignmentService(session, rule_service)
    availability_service = AvailabilityService(session)
    audit_service = AuditService(session)
    publication_service = PublicationService(session, audit_service)
    auto_assign_service = AutoAssignJobService(session, assignment_service)
    return {
        "templates": template_service,
        "instances": instance_service,
        "assignments": assignment_service,
        "availability": availability_service,
        "audit": audit_service,
        "publication": publication_service,
        "auto_assign": auto_assign_service,
        "rules": rule_service,
    }


PlanningServicesDep = Annotated[dict[str, object], Depends(get_planning_services)]


@router.get("/shift-templates", response_model=list[ShiftTemplate])
def list_shift_templates(
    services: PlanningServicesDep, mission_id: int | None = Query(default=None)
) -> list[ShiftTemplate]:
    template_service: ShiftTemplateService = services["templates"]  # type: ignore[assignment]
    return template_service.list_templates(mission_id=mission_id)


@router.post(
    "/shift-templates",
    response_model=ShiftTemplate,
    status_code=status.HTTP_201_CREATED,
)
def create_shift_template(
    payload: ShiftTemplateCreate,
    services: PlanningServicesDep,
) -> ShiftTemplate:
    template_service: ShiftTemplateService = services["templates"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    template = template_service.create_template(payload)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_template",
        entity_id=template.id,
        action="create_shift_template",
        before=None,
        after=template.model_dump(),
    )
    return template


@router.put("/shift-templates/{template_id}", response_model=ShiftTemplate)
def update_shift_template(
    template_id: int,
    payload: ShiftTemplateUpdate,
    services: PlanningServicesDep,
) -> ShiftTemplate:
    template_service: ShiftTemplateService = services["templates"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    before = template_service.get_template_state(template_id).model_dump()
    updated = template_service.update_template(template_id, payload)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_template",
        entity_id=template_id,
        action="update_shift_template",
        before=before,
        after=updated.model_dump(),
    )
    return updated


@router.delete("/shift-templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift_template(
    template_id: int,
    services: PlanningServicesDep,
) -> None:
    template_service: ShiftTemplateService = services["templates"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    before = template_service.get_template_state(template_id).model_dump()
    template_service.delete_template(template_id)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_template",
        entity_id=template_id,
        action="delete_shift_template",
        before=before,
        after=None,
    )


@router.get("/shifts", response_model=list[ShiftWithAssignments])
def list_shift_instances(
    services: PlanningServicesDep, mission_id: int | None = Query(default=None)
) -> list[ShiftWithAssignments]:
    instance_service: ShiftInstanceService = services["instances"]  # type: ignore[assignment]
    return instance_service.list_instances(mission_id=mission_id)


@router.post("/shifts", response_model=ShiftWriteResponse, status_code=status.HTTP_201_CREATED)
def create_shift_instance(
    payload: ShiftInstanceCreate,
    services: PlanningServicesDep,
) -> ShiftWriteResponse:
    instance_service: ShiftInstanceService = services["instances"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    shift_view = instance_service.create_instance(payload)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_instance",
        entity_id=shift_view.shift.id,
        action="create_shift",
        before=None,
        after=shift_view.shift.model_dump(),
    )
    return ShiftWriteResponse(shift=shift_view.shift, conflicts=shift_view.conflicts)


@router.get("/shift-instances", response_model=list[ShiftWithAssignments])
def filter_shift_instances(
    services: PlanningServicesDep,
    start: Annotated[datetime | None, Query()] = None,
    end: Annotated[datetime | None, Query()] = None,
    place_ids: Annotated[list[int] | None, Query(alias="place_ids")] = None,
    person_ids: Annotated[list[int] | None, Query(alias="person_ids")] = None,
    status: Annotated[list[str] | None, Query(alias="status")] = None,
) -> list[ShiftWithAssignments]:
    instance_service: ShiftInstanceService = services["instances"]  # type: ignore[assignment]
    return instance_service.list_instances(
        start=start,
        end=end,
        site_ids=place_ids,
        collaborator_ids=person_ids,
        statuses=status,
    )


@router.put("/shifts/{shift_id}", response_model=ShiftWriteResponse)
def update_shift_instance(
    shift_id: int,
    payload: ShiftInstanceUpdate,
    services: PlanningServicesDep,
) -> ShiftWriteResponse:
    instance_service: ShiftInstanceService = services["instances"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    before = instance_service.get_instance_state(shift_id).model_dump()
    shift_view = instance_service.update_instance(shift_id, payload)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_instance",
        entity_id=shift_id,
        action="update_shift",
        before=before,
        after=shift_view.shift.model_dump(),
    )
    return ShiftWriteResponse(shift=shift_view.shift, conflicts=shift_view.conflicts)


@router.put("/shift-instances/{shift_id}", response_model=ShiftWriteResponse)
def update_shift_instance_alias(
    shift_id: int,
    payload: ShiftInstanceUpdate,
    services: PlanningServicesDep,
) -> ShiftWriteResponse:
    return update_shift_instance(shift_id, payload, services)


@router.delete("/shifts/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift_instance(
    shift_id: int,
    services: PlanningServicesDep,
) -> None:
    instance_service: ShiftInstanceService = services["instances"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    before = instance_service.get_instance_state(shift_id).model_dump()
    instance_service.delete_instance(shift_id)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_instance",
        entity_id=shift_id,
        action="delete_shift",
        before=before,
        after=None,
    )


@router.get("/assignments", response_model=list[Assignment])
def list_assignments(
    services: PlanningServicesDep, instance_id: int | None = Query(default=None)
) -> list[Assignment]:
    assignment_service: AssignmentService = services["assignments"]  # type: ignore[assignment]
    return assignment_service.list_assignments(instance_id=instance_id)


@router.post(
    "/assignments",
    response_model=AssignmentWriteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_assignment(
    payload: AssignmentCreate,
    services: PlanningServicesDep,
) -> AssignmentWriteResponse:
    assignment_service: AssignmentService = services["assignments"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    assignment, conflicts = assignment_service.create_assignment(payload)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="assignment",
        entity_id=assignment.id,
        action="create_assignment",
        before=None,
        after=assignment.model_dump(),
    )
    return AssignmentWriteResponse(assignment=assignment, conflicts=conflicts)


@router.put("/assignments/{assignment_id}", response_model=AssignmentWriteResponse)
def update_assignment(
    assignment_id: int,
    payload: AssignmentUpdate,
    services: PlanningServicesDep,
) -> AssignmentWriteResponse:
    assignment_service: AssignmentService = services["assignments"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    before = assignment_service.get_assignment_state(assignment_id).model_dump()
    assignment, conflicts = assignment_service.update_assignment(assignment_id, payload)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="assignment",
        entity_id=assignment_id,
        action="update_assignment",
        before=before,
        after=assignment.model_dump(),
    )
    return AssignmentWriteResponse(assignment=assignment, conflicts=conflicts)


@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(
    assignment_id: int,
    services: PlanningServicesDep,
) -> None:
    assignment_service: AssignmentService = services["assignments"]  # type: ignore[assignment]
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    before = assignment_service.get_assignment_state(assignment_id).model_dump()
    assignment_service.delete_assignment(assignment_id)
    audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="assignment",
        entity_id=assignment_id,
        action="delete_assignment",
        before=before,
        after=None,
    )


@router.get("/availability", response_model=list[UserAvailability])
def list_availability(
    services: PlanningServicesDep, collaborator_id: int | None = Query(default=None)
) -> list[UserAvailability]:
    availability_service: AvailabilityService = services["availability"]  # type: ignore[assignment]
    return availability_service.list_availability(collaborator_id=collaborator_id)


@router.post(
    "/availability",
    response_model=UserAvailability,
    status_code=status.HTTP_201_CREATED,
)
def create_availability(
    payload: UserAvailabilityCreate,
    services: PlanningServicesDep,
) -> UserAvailability:
    availability_service: AvailabilityService = services["availability"]  # type: ignore[assignment]
    return availability_service.record_availability(payload)


@router.get("/rules")
def list_rules(
    services: PlanningServicesDep, organization_id: int = Query(default=1)
) -> dict[str, list[HrRule] | list[ConflictRule]]:
    rule_service: RuleService = services["rules"]  # type: ignore[assignment]
    hr_rules = rule_service.list_hr_rules(organization_id)
    conflict_rules = rule_service.list_conflict_rules(organization_id)
    return {"hr_rules": hr_rules, "conflict_rules": conflict_rules}


@router.post("/conflicts/preview", response_model=list[ConflictPreviewResult])
def preview_conflicts(
    payload: ConflictPreviewPayload,
    services: PlanningServicesDep,
) -> list[ConflictPreviewResult]:
    rule_service: RuleService = services["rules"]  # type: ignore[assignment]
    results: list[ConflictPreviewResult] = []
    if payload.shift is not None:
        results.append(
            ConflictPreviewResult(
                shift=payload.shift,
                conflicts=rule_service.evaluate_shift(payload.shift),
            )
        )
    for assignment in payload.assignments or []:
        results.append(
            ConflictPreviewResult(
                assignment=assignment,
                conflicts=rule_service.evaluate_assignment(assignment),
            )
        )
    return results


@router.post("/publish", response_model=Publication)
def publish_planning(
    payload: PublishRequest,
    services: PlanningServicesDep,
) -> Publication:
    publication_service: PublicationService = services["publication"]  # type: ignore[assignment]
    publication = publication_service.prepare_draft(organization_id=1, message=payload.message)
    published = publication_service.publish(publication.id)
    return published


@router.post("/auto-assign/start")
def start_auto_assign(
    payload: AutoAssignStartRequest, services: PlanningServicesDep
) -> dict[str, Any]:
    auto_assign_service: AutoAssignJobService = services["auto_assign"]  # type: ignore[assignment]
    return auto_assign_service.start_job(shift_ids=payload.shift_ids)


@router.get("/auto-assign/status/{job_id}")
def get_auto_assign_status(
    job_id: str,
    services: PlanningServicesDep,
) -> dict[str, Any]:
    auto_assign_service: AutoAssignJobService = services["auto_assign"]  # type: ignore[assignment]
    return auto_assign_service.get_status(job_id)


@router.get("/audit", response_model=list[dict[str, Any]])
def list_audit_trail(
    services: PlanningServicesDep,
    from_ts: Annotated[datetime | None, Query()] = None,
    to_ts: Annotated[datetime | None, Query()] = None,
    entity: Annotated[str | None, Query()] = None,
    entity_id: Annotated[int | None, Query()] = None,
) -> list[dict[str, Any]]:
    audit_service: AuditService = services["audit"]  # type: ignore[assignment]
    return audit_service.list_changes(
        from_ts=from_ts, to_ts=to_ts, entity_type=entity, entity_id=entity_id
    )
