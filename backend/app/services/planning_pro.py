"""Planning PRO service skeletons for Phase 5 foundations."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Any

from app.models.planning_pro import (
    Assignment,
    AssignmentCreate,
    ConflictRule,
    HrRule,
    NotificationEvent,
    Publication,
    ShiftInstance,
    ShiftInstanceCreate,
    ShiftTemplate,
    ShiftTemplateCreate,
    UserAvailability,
    UserAvailabilityCreate,
)


class ShiftTemplateService:
    """Manage shift templates and derived instances."""

    def list_templates(self, *, mission_id: int | None = None) -> list[ShiftTemplate]:
        """Return stored templates, optionally filtered by mission."""
        raise NotImplementedError

    def create_template(self, payload: ShiftTemplateCreate) -> ShiftTemplate:
        """Create a template with recurrence and base staffing needs."""
        raise NotImplementedError

    def deactivate_template(self, template_id: int) -> None:
        """Soft-deactivate a template without deleting historical instances."""
        raise NotImplementedError


class ShiftInstanceService:
    """Manage concrete shift instances generated from templates or ad hoc."""

    def list_instances(self, *, mission_id: int | None = None) -> list[ShiftInstance]:
        raise NotImplementedError

    def create_instance(self, payload: ShiftInstanceCreate) -> ShiftInstance:
        raise NotImplementedError

    def update_status(self, instance_id: int, *, status: str) -> ShiftInstance:
        """Promote a draft instance to published or cancel it with validation hooks."""
        raise NotImplementedError


class AssignmentService:
    """Handle collaborator assignments on shift instances."""

    def list_assignments(self, *, instance_id: int | None = None) -> list[Assignment]:
        raise NotImplementedError

    def create_assignment(self, payload: AssignmentCreate) -> Assignment:
        raise NotImplementedError

    def bulk_upsert(self, payloads: Iterable[AssignmentCreate]) -> list[Assignment]:
        """Prepare the surface for auto-assign jobs and manual batch edits."""
        raise NotImplementedError

    def lock(self, assignment_id: int, *, locked: bool) -> Assignment:
        raise NotImplementedError


class AvailabilityService:
    """Track user availability, leaves and blackout overlays."""

    def record_availability(self, payload: UserAvailabilityCreate) -> UserAvailability:
        raise NotImplementedError

    def list_availability(self, *, collaborator_id: int | None = None) -> list[UserAvailability]:
        raise NotImplementedError

    def record_leave(
        self, *, collaborator_id: int, start: datetime, end: datetime, category: str
    ) -> None:
        raise NotImplementedError


class RuleService:
    """Evaluate HR and conflict rules for planning validation."""

    def list_hr_rules(self, organization_id: int) -> list[HrRule]:
        raise NotImplementedError

    def list_conflict_rules(self, organization_id: int) -> list[ConflictRule]:
        raise NotImplementedError

    def evaluate_instance(self, instance: ShiftInstance) -> list[str]:
        """Return rule identifiers violated by the instance assignments."""
        raise NotImplementedError


class AuditService:
    """Log planning changes for auditability."""

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
        raise NotImplementedError


class PublicationService:
    """Create and publish planning snapshots."""

    def prepare_draft(self, organization_id: int, message: str | None = None) -> Publication:
        raise NotImplementedError

    def publish(self, publication_id: int) -> Publication:
        raise NotImplementedError

    def list_events(self, organization_id: int) -> list[NotificationEvent]:
        raise NotImplementedError
