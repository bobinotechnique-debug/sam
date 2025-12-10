from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: dict[str, Any] | list[Any] | None = None
    trace_id: str
