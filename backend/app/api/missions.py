from fastapi import APIRouter, Query, status

from app.api.errors import map_service_error
from app.models.common import PaginatedResponse
from app.models.mission import Mission, MissionCreate, MissionUpdate
from app.services.errors import ServiceError
from app.services.registry import mission_service

router = APIRouter(prefix="/api/v1/missions", tags=["missions"])


@router.get("", response_model=PaginatedResponse[Mission])
def list_missions(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)
) -> PaginatedResponse[Mission]:
    return mission_service.list(page, page_size)


@router.post("", response_model=Mission, status_code=status.HTTP_201_CREATED)
def create_mission(payload: MissionCreate) -> Mission:
    try:
        return mission_service.create(payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.get("/{mission_id}", response_model=Mission)
def get_mission(mission_id: int) -> Mission:
    try:
        return mission_service.get(mission_id)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.patch("/{mission_id}", response_model=Mission)
def update_mission(mission_id: int, payload: MissionUpdate) -> Mission:
    try:
        return mission_service.update(mission_id, payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int) -> None:
    try:
        mission_service.delete(mission_id)
    except ServiceError as error:
        raise map_service_error(error) from error
