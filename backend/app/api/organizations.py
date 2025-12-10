from fastapi import APIRouter, Query, status

from app.models.common import PaginatedResponse
from app.models.organization import Organization, OrganizationCreate, OrganizationUpdate
from app.services.registry import organization_service

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


@router.get("", response_model=PaginatedResponse[Organization])
def list_organizations(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)
) -> PaginatedResponse[Organization]:
    return organization_service.list(page, page_size)


@router.post("", response_model=Organization, status_code=status.HTTP_201_CREATED)
def create_organization(payload: OrganizationCreate) -> Organization:
    return organization_service.create(payload)


@router.get("/{organization_id}", response_model=Organization)
def get_organization(organization_id: int) -> Organization:
    return organization_service.get(organization_id)


@router.patch("/{organization_id}", response_model=Organization)
def update_organization(organization_id: int, payload: OrganizationUpdate) -> Organization:
    return organization_service.update(organization_id, payload)


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(organization_id: int) -> None:
    organization_service.delete(organization_id)
