from fastapi import APIRouter, Query, status

from app.models.common import PaginatedResponse
from app.models.mission import Mission, MissionCreate, MissionUpdate
from app.services.registry import mission_service

router = APIRouter(prefix="/api/v1/missions", tags=["missions"])


@router.get("", response_model=PaginatedResponse[Mission])
def list_missions(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)
) -> PaginatedResponse[Mission]:
    return mission_service.list(page, page_size)


@router.post("", response_model=Mission, status_code=status.HTTP_201_CREATED)
def create_mission(payload: MissionCreate) -> Mission:
    return mission_service.create(payload)


@router.get("/{mission_id}", response_model=Mission)
def get_mission(mission_id: int) -> Mission:
    return mission_service.get(mission_id)


@router.patch("/{mission_id}", response_model=Mission)
def update_mission(mission_id: int, payload: MissionUpdate) -> Mission:
    return mission_service.update(mission_id, payload)


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int) -> None:
    mission_service.delete(mission_id)
