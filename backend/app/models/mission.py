from datetime import UTC, datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.common import TimeWindow


class MissionBase(TimeWindow):
    site_id: int
    role_id: int
    status: str = Field(default="draft", pattern="^(draft|published|cancelled)$")
    budget_target: float | None = Field(default=None, ge=0)
    note: str | None = Field(default=None, max_length=500)


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    site_id: int | None = None
    role_id: int | None = None
    status: str | None = Field(default=None, pattern="^(draft|published|cancelled)$")
    start_utc: datetime | None = None
    end_utc: datetime | None = None
    budget_target: float | None = Field(default=None, ge=0)
    note: str | None = Field(default=None, max_length=500)

    @field_validator("start_utc", "end_utc")
    @classmethod
    def ensure_timezone(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("Datetime must include timezone information")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_window(self) -> "MissionUpdate":
        if (
            self.start_utc is not None
            and self.end_utc is not None
            and self.start_utc >= self.end_utc
        ):
            raise ValueError("start_utc must be earlier than end_utc")
        return self


class Mission(MissionBase):
    id: int

    model_config = {"extra": "forbid"}
