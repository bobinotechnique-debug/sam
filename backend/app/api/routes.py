from fastapi import APIRouter, HTTPException, status

from app.core.logging import logger
from app.models.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import item_service

router = APIRouter()


@router.get("/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    logger.info("Healthcheck requested")
    return {"status": "ok"}


@router.get("/items", response_model=list[Item], tags=["items"])
def list_items() -> list[Item]:
    return item_service.list_items()


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item(payload: ItemCreate) -> Item:
    created = item_service.create_item(payload)
    logger.info("Item created", extra={"item_id": created.id})
    return created


@router.get("/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int) -> Item:
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, payload: ItemUpdate) -> Item:
    updated = item_service.update_item(item_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    logger.info("Item updated", extra={"item_id": item_id})
    return updated


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int) -> None:
    deleted = item_service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    logger.info("Item deleted", extra={"item_id": item_id})
