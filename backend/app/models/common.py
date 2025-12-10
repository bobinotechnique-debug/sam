from datetime import UTC, datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator, model_validator

ItemType = TypeVar("ItemType")


class PaginatedResponse(BaseModel, Generic[ItemType]):
    items: list[ItemType]
    total: int
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)


class TimeWindow(BaseModel):
    start_utc: datetime
    end_utc: datetime

    @field_validator("start_utc", "end_utc")
    @classmethod
    def ensure_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Datetime must include timezone information")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_order(self) -> "TimeWindow":
        if self.start_utc >= self.end_utc:
            raise ValueError("start_utc must be earlier than end_utc")
        return self
