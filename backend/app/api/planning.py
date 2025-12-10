from typing import Any

from fastapi import APIRouter, Query, status
from pydantic import BaseModel

from app.models.planning_pro import (
    Assignment,
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentWriteResponse,
    ConflictEntry,
    ConflictRule,
    HrRule,
    Publication,
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
from app.services.registry import (
    planning_assignment_service,
    planning_audit_service,
    planning_auto_assign_service,
    planning_availability_service,
    planning_publication_service,
    planning_rule_service,
    planning_shift_instance_service,
    planning_shift_template_service,
)

router = APIRouter(prefix="/api/v1/planning", tags=["planning_pro"])


class ConflictPreviewPayload(BaseModel):
    shift: ShiftInstanceCreate | None = None
    assignments: list[AssignmentCreate] | None = None


class PublishRequest(BaseModel):
    message: str | None = None


@router.get("/shift-templates", response_model=list[ShiftTemplate])
def list_shift_templates(mission_id: int | None = Query(default=None)) -> list[ShiftTemplate]:
    return planning_shift_template_service.list_templates(mission_id=mission_id)


@router.post(
    "/shift-templates",
    response_model=ShiftTemplate,
    status_code=status.HTTP_201_CREATED,
)
def create_shift_template(payload: ShiftTemplateCreate) -> ShiftTemplate:
    template = planning_shift_template_service.create_template(payload)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_template",
        entity_id=template.id,
        action="create_shift_template",
        payload=payload.model_dump(),
    )
    return template


@router.put("/shift-templates/{template_id}", response_model=ShiftTemplate)
def update_shift_template(template_id: int, payload: ShiftTemplateUpdate) -> ShiftTemplate:
    updated = planning_shift_template_service.update_template(template_id, payload)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_template",
        entity_id=template_id,
        action="update_shift_template",
        payload=payload.model_dump(exclude_none=True),
    )
    return updated


@router.delete("/shift-templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift_template(template_id: int) -> None:
    planning_shift_template_service.delete_template(template_id)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_template",
        entity_id=template_id,
        action="delete_shift_template",
        payload={},
    )


@router.get("/shifts", response_model=list[ShiftWithAssignments])
def list_shift_instances(
    mission_id: int | None = Query(default=None),
) -> list[ShiftWithAssignments]:
    return planning_shift_instance_service.list_instances(mission_id=mission_id)


@router.post("/shifts", response_model=ShiftWriteResponse, status_code=status.HTTP_201_CREATED)
def create_shift_instance(payload: ShiftInstanceCreate) -> ShiftWriteResponse:
    shift_view = planning_shift_instance_service.create_instance(payload)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_instance",
        entity_id=shift_view.shift.id,
        action="create_shift",
        payload=payload.model_dump(),
    )
    return ShiftWriteResponse(shift=shift_view.shift, conflicts=shift_view.conflicts)


@router.put("/shifts/{shift_id}", response_model=ShiftWriteResponse)
def update_shift_instance(shift_id: int, payload: ShiftInstanceUpdate) -> ShiftWriteResponse:
    shift_view = planning_shift_instance_service.update_instance(shift_id, payload)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_instance",
        entity_id=shift_id,
        action="update_shift",
        payload=payload.model_dump(exclude_none=True),
    )
    return ShiftWriteResponse(shift=shift_view.shift, conflicts=shift_view.conflicts)


@router.delete("/shifts/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift_instance(shift_id: int) -> None:
    planning_shift_instance_service.delete_instance(shift_id)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="shift_instance",
        entity_id=shift_id,
        action="delete_shift",
        payload={},
    )


@router.get("/assignments", response_model=list[Assignment])
def list_assignments(instance_id: int | None = Query(default=None)) -> list[Assignment]:
    return planning_assignment_service.list_assignments(instance_id=instance_id)


@router.post(
    "/assignments",
    response_model=AssignmentWriteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_assignment(payload: AssignmentCreate) -> AssignmentWriteResponse:
    assignment, conflicts = planning_assignment_service.create_assignment(payload)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="assignment",
        entity_id=assignment.id,
        action="create_assignment",
        payload=payload.model_dump(),
    )
    return AssignmentWriteResponse(assignment=assignment, conflicts=conflicts)


@router.put("/assignments/{assignment_id}", response_model=AssignmentWriteResponse)
def update_assignment(assignment_id: int, payload: AssignmentUpdate) -> AssignmentWriteResponse:
    assignment, conflicts = planning_assignment_service.update_assignment(assignment_id, payload)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="assignment",
        entity_id=assignment_id,
        action="update_assignment",
        payload=payload.model_dump(exclude_none=True),
    )
    return AssignmentWriteResponse(assignment=assignment, conflicts=conflicts)


@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int) -> None:
    planning_assignment_service.delete_assignment(assignment_id)
    planning_audit_service.log_change(
        organization_id=1,
        actor_user_id=None,
        entity_type="assignment",
        entity_id=assignment_id,
        action="delete_assignment",
        payload={},
    )


@router.get("/availability", response_model=list[UserAvailability])
def list_availability(collaborator_id: int | None = Query(default=None)) -> list[UserAvailability]:
    return planning_availability_service.list_availability(collaborator_id=collaborator_id)


@router.post("/availability", response_model=UserAvailability, status_code=status.HTTP_201_CREATED)
def record_availability(payload: UserAvailabilityCreate) -> UserAvailability:
    availability = planning_availability_service.record_availability(payload)
    return availability


@router.get("/rules")
def list_rules(organization_id: int = Query(default=1)) -> dict[str, list[HrRule] | list[ConflictRule]]:
    hr_rules = planning_rule_service.list_hr_rules(organization_id)
    conflict_rules = planning_rule_service.list_conflict_rules(organization_id)
    return {"hr_rules": hr_rules, "conflict_rules": conflict_rules}


@router.post("/conflicts/preview", response_model=list[ConflictEntry])
def preview_conflicts(payload: ConflictPreviewPayload) -> list[ConflictEntry]:
    conflicts: list[ConflictEntry] = []
    if payload.shift is not None:
        conflicts.extend(planning_rule_service.evaluate_shift(payload.shift))
    for assignment in payload.assignments or []:
        conflicts.extend(planning_rule_service.evaluate_assignment(assignment))
    return conflicts


@router.post("/publish", response_model=Publication)
def publish_planning(payload: PublishRequest) -> Publication:
    publication = planning_publication_service.prepare_draft(
        organization_id=1, message=payload.message
    )
    published = planning_publication_service.publish(publication.id)
    return published


@router.post("/auto-assign/start")
def start_auto_assign(shift_ids: list[int] | None = None) -> dict[str, Any]:
    return planning_auto_assign_service.start_job(shift_ids=shift_ids)


@router.get("/auto-assign/status/{job_id}")
def get_auto_assign_status(job_id: str) -> dict[str, Any]:
    return planning_auto_assign_service.get_status(job_id)


@router.get("/audit", response_model=list[dict[str, Any]])
def list_audit_trail() -> list[dict[str, Any]]:
    return planning_audit_service.list_changes()
