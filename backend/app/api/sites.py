from fastapi import APIRouter, Query, status

from app.models.common import PaginatedResponse
from app.models.site import Site, SiteCreate, SiteUpdate
from app.services.registry import site_service

router = APIRouter(prefix="/api/v1/sites", tags=["sites"])


@router.get("", response_model=PaginatedResponse[Site])
def list_sites(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)
) -> PaginatedResponse[Site]:
    return site_service.list(page, page_size)


@router.post("", response_model=Site, status_code=status.HTTP_201_CREATED)
def create_site(payload: SiteCreate) -> Site:
    return site_service.create(payload)


@router.get("/{site_id}", response_model=Site)
def get_site(site_id: int) -> Site:
    return site_service.get(site_id)


@router.patch("/{site_id}", response_model=Site)
def update_site(site_id: int, payload: SiteUpdate) -> Site:
    return site_service.update(site_id, payload)


@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_site(site_id: int) -> None:
    site_service.delete(site_id)
