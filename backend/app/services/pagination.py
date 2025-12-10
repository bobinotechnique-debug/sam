from collections.abc import Sequence
from typing import TypeVar

from app.models.common import PaginatedResponse

ItemType = TypeVar("ItemType")


def paginate(items: Sequence[ItemType], page: int, page_size: int) -> PaginatedResponse[ItemType]:
    start = (page - 1) * page_size
    end = start + page_size
    return PaginatedResponse(
        items=list(items)[start:end],
        total=len(items),
        page=page,
        page_size=page_size,
    )
