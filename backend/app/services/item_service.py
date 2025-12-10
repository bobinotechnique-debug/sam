from app.models.item import Item, ItemCreate, ItemUpdate


class InMemoryItemService:
    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._counter = 0

    def list_items(self) -> list[Item]:
        return list(self._items.values())

    def create_item(self, payload: ItemCreate) -> Item:
        self._counter += 1
        item = Item(id=self._counter, name=payload.name, description=payload.description)
        self._items[item.id] = item
        return item

    def get_item(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def update_item(self, item_id: int, payload: ItemUpdate) -> Item | None:
        existing = self._items.get(item_id)
        if existing is None:
            return None
        updated = existing.model_copy(update=payload.model_dump(exclude_none=True))
        self._items[item_id] = updated
        return updated

    def delete_item(self, item_id: int) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False

    def reset(self) -> None:
        self._items.clear()
        self._counter = 0


item_service = InMemoryItemService()
