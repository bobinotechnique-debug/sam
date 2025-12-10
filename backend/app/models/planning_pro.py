from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.common import TimeWindow


class ShiftTemplateBase(BaseModel):
    mission_id: int
    site_id: int
    role_id: int
    team_id: int | None = None
    recurrence_rule: str | None = Field(default=None, max_length=255)
    start_time_utc: datetime
    end_time_utc: datetime
    expected_headcount: int = Field(default=1, ge=1)
    is_active: bool = True

    @field_validator("start_time_utc", "end_time_utc")
    @classmethod
    def ensure_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Datetime must include timezone information")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_window(self) -> "ShiftTemplateBase":
        if self.start_time_utc >= self.end_time_utc:
            raise ValueError("start_time_utc must be earlier than end_time_utc")
        return self


class ShiftTemplateCreate(ShiftTemplateBase):
    pass


class ShiftTemplate(ShiftTemplateBase):
    id: int

    model_config = {"extra": "forbid"}


class ShiftTemplateUpdate(BaseModel):
    mission_id: int | None = None
    site_id: int | None = None
    role_id: int | None = None
    team_id: int | None = None
    recurrence_rule: str | None = Field(default=None, max_length=255)
    start_time_utc: datetime | None = None
    end_time_utc: datetime | None = None
    expected_headcount: int | None = Field(default=None, ge=1)
    is_active: bool | None = None

    @field_validator("start_time_utc", "end_time_utc")
    @classmethod
    def ensure_timezone(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("Datetime must include timezone information")
        return value.astimezone(UTC)


class ShiftInstanceBase(TimeWindow):
    mission_id: int
    template_id: int | None = None
    site_id: int
    role_id: int
    team_id: int | None = None
    status: str = Field(default="draft", pattern="^(draft|published|cancelled)$")
    source: str = Field(default="manual", max_length=50)
    capacity: int = Field(default=1, ge=1)


class ShiftInstanceCreate(ShiftInstanceBase):
    pass


class ShiftInstance(ShiftInstanceBase):
    id: int

    model_config = {"extra": "forbid"}


class ShiftInstanceUpdate(BaseModel):
    mission_id: int | None = None
    template_id: int | None = None
    site_id: int | None = None
    role_id: int | None = None
    team_id: int | None = None
    start_utc: datetime | None = None
    end_utc: datetime | None = None
    status: str | None = Field(default=None, pattern="^(draft|published|cancelled)$")
    source: str | None = Field(default=None, max_length=50)
    capacity: int | None = Field(default=None, ge=1)

    @field_validator("start_utc", "end_utc")
    @classmethod
    def ensure_timezone(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("Datetime must include timezone information")
        return value.astimezone(UTC)


class AssignmentBase(BaseModel):
    shift_instance_id: int
    collaborator_id: int
    role_id: int
    status: str = Field(default="proposed", pattern="^(proposed|confirmed|rejected)$")
    source: str = Field(default="manual", max_length=50)
    note: str | None = Field(default=None, max_length=500)
    is_locked: bool = False


class AssignmentCreate(AssignmentBase):
    pass


class Assignment(AssignmentBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"extra": "forbid"}


class AssignmentUpdate(BaseModel):
    collaborator_id: int | None = None
    role_id: int | None = None
    status: str | None = Field(default=None, pattern="^(proposed|confirmed|rejected)$")
    source: str | None = Field(default=None, max_length=50)
    note: str | None = Field(default=None, max_length=500)
    is_locked: bool | None = None


class UserAvailabilityBase(TimeWindow):
    collaborator_id: int
    is_available: bool = True
    reason: str | None = Field(default=None, max_length=255)


class UserAvailabilityCreate(UserAvailabilityBase):
    pass


class UserAvailability(UserAvailabilityBase):
    id: int

    model_config = {"extra": "forbid"}


class HrRule(BaseModel):
    id: int
    organization_id: int
    code: str = Field(max_length=120)
    severity: str = Field(default="hard", pattern="^(hard|soft)$")
    description: str | None = Field(default=None, max_length=255)
    config: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "forbid"}


class ConflictRule(BaseModel):
    id: int
    organization_id: int
    code: str = Field(max_length=120)
    severity: str = Field(default="error", pattern="^(error|warning)$")
    description: str | None = Field(default=None, max_length=255)
    config: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "forbid"}


class Publication(BaseModel):
    id: int
    organization_id: int
    author_user_id: int | None = None
    status: str = Field(default="draft", pattern="^(draft|published)$")
    version: int = Field(default=1, ge=1)
    message: str | None = Field(default=None, max_length=255)
    published_at: datetime | None = None

    model_config = {"extra": "forbid"}


class NotificationEvent(BaseModel):
    id: int
    organization_id: int
    recipient_user_id: int | None = None
    event_type: str = Field(max_length=100)
    payload: dict[str, Any] = Field(default_factory=dict)
    related_shift_instance_id: int | None = None
    created_at: datetime | None = None
    read_at: datetime | None = None

    model_config = {"extra": "forbid"}


class ConflictEntry(BaseModel):
    type: str = Field(pattern="^(hard|soft)$")
    rule: str
    details: dict[str, Any] = Field(default_factory=dict)


class ShiftWithAssignments(BaseModel):
    shift: ShiftInstance
    assignments: list[Assignment] = Field(default_factory=list)
    conflicts: list[ConflictEntry] = Field(default_factory=list)


class ShiftWriteResponse(BaseModel):
    shift: ShiftInstance
    conflicts: list[ConflictEntry] = Field(default_factory=list)


class AssignmentWriteResponse(BaseModel):
    assignment: Assignment
    conflicts: list[ConflictEntry] = Field(default_factory=list)
