from fastapi import APIRouter, Query, status

from app.api.errors import map_service_error
from app.models.common import PaginatedResponse
from app.models.shift import Shift, ShiftCreate, ShiftUpdate
from app.services.errors import ServiceError
from app.services.registry import shift_service

router = APIRouter(prefix="/api/v1/shifts", tags=["shifts"])


@router.get("", response_model=PaginatedResponse[Shift])
def list_shifts(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)
) -> PaginatedResponse[Shift]:
    return shift_service.list(page, page_size)


@router.post("", response_model=Shift, status_code=status.HTTP_201_CREATED)
def create_shift(payload: ShiftCreate) -> Shift:
    try:
        return shift_service.create(payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.get("/{shift_id}", response_model=Shift)
def get_shift(shift_id: int) -> Shift:
    try:
        return shift_service.get(shift_id)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.patch("/{shift_id}", response_model=Shift)
def update_shift(shift_id: int, payload: ShiftUpdate) -> Shift:
    try:
        return shift_service.update(shift_id, payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.delete("/{shift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shift(shift_id: int) -> None:
    try:
        shift_service.delete(shift_id)
    except ServiceError as error:
        raise map_service_error(error) from error
