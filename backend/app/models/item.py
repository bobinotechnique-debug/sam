from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int = Field(..., description="Unique identifier")
    name: str = Field(..., min_length=1, description="Display name")
    description: str = Field(default="", description="Optional details")


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(default="")


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None)


def item_to_dict(item: Item) -> dict[str, str | int]:
    return item.model_dump()
