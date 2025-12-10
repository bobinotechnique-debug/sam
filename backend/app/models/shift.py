from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.common import TimeWindow


class ShiftBase(TimeWindow):
    mission_id: int
    collaborator_id: int
    status: str = Field(default="draft", pattern="^(draft|confirmed|cancelled)$")
    cancellation_reason: str | None = Field(default=None, max_length=300)


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(BaseModel):
    mission_id: int | None = None
    collaborator_id: int | None = None
    status: str | None = Field(default=None, pattern="^(draft|confirmed|cancelled)$")
    start_utc: datetime | None = None
    end_utc: datetime | None = None
    cancellation_reason: str | None = Field(default=None, max_length=300)

    @field_validator("start_utc", "end_utc")
    @classmethod
    def ensure_timezone(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("Datetime must include timezone information")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_window(self) -> "ShiftUpdate":
        if (
            self.start_utc is not None
            and self.end_utc is not None
            and self.start_utc >= self.end_utc
        ):
            raise ValueError("start_utc must be earlier than end_utc")
        return self


class Shift(ShiftBase):
    id: int

    model_config = {"extra": "forbid"}
