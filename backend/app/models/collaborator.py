from pydantic import BaseModel, Field


class CollaboratorBase(BaseModel):
    organization_id: int
    full_name: str = Field(..., min_length=1, max_length=200)
    primary_role_id: int | None = None
    status: str = Field(default="active", pattern="^(active|inactive)$")
    email: str | None = Field(default=None, max_length=255)


class CollaboratorCreate(CollaboratorBase):
    pass


class CollaboratorUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    primary_role_id: int | None = None
    status: str | None = Field(default=None, pattern="^(active|inactive)$")
    email: str | None = Field(default=None, max_length=255)


class Collaborator(CollaboratorBase):
    id: int

    model_config = {"extra": "forbid"}
