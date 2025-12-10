from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator


def _validate_timezone(value: str | None) -> str | None:
    if value is None:
        return None
    ZoneInfo(value)  # raises if invalid
    return value


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    timezone: str = Field(default="UTC")
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    contact_email: str | None = Field(default=None, max_length=255)

    _tz_validator = field_validator("timezone", mode="before")(_validate_timezone)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    timezone: str | None = Field(default=None)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    contact_email: str | None = Field(default=None, max_length=255)

    _tz_validator = field_validator("timezone", mode="before")(_validate_timezone)


class Organization(OrganizationBase):
    id: int

    model_config = {"extra": "forbid"}
