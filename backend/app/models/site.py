from pydantic import BaseModel, Field, field_validator

from app.models.organization import _validate_timezone


class SiteBase(BaseModel):
    organization_id: int
    name: str = Field(..., min_length=1, max_length=200)
    timezone: str | None = Field(default=None)
    address: str | None = Field(default=None, max_length=255)

    _tz_validator = field_validator("timezone", mode="before", check_fields=False)(
        _validate_timezone
    )


class SiteCreate(SiteBase):
    pass


class SiteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    timezone: str | None = Field(default=None)
    address: str | None = Field(default=None, max_length=255)

    _tz_validator = field_validator("timezone", mode="before", check_fields=False)(
        _validate_timezone
    )


class Site(SiteBase):
    id: int
    timezone: str

    model_config = {"extra": "forbid"}
