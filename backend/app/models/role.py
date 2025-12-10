from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    organization_id: int
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    tags: list[str] = Field(default_factory=list)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)
    tags: list[str] | None = None


class Role(RoleBase):
    id: int

    model_config = {"extra": "forbid"}
