from fastapi import APIRouter, Query, status

from app.api.errors import map_service_error
from app.models.common import PaginatedResponse
from app.models.site import Site, SiteCreate, SiteUpdate
from app.services.errors import ServiceError
from app.services.registry import site_service

router = APIRouter(prefix="/api/v1/sites", tags=["sites"])


@router.get("", response_model=PaginatedResponse[Site])
def list_sites(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)
) -> PaginatedResponse[Site]:
    return site_service.list(page, page_size)


@router.post("", response_model=Site, status_code=status.HTTP_201_CREATED)
def create_site(payload: SiteCreate) -> Site:
    try:
        return site_service.create(payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.get("/{site_id}", response_model=Site)
def get_site(site_id: int) -> Site:
    try:
        return site_service.get(site_id)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.patch("/{site_id}", response_model=Site)
def update_site(site_id: int, payload: SiteUpdate) -> Site:
    try:
        return site_service.update(site_id, payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int) -> None:
    try:
        site_service.delete(site_id)
    except ServiceError as error:
        raise map_service_error(error) from error
