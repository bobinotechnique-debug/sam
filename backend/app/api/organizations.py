from fastapi import APIRouter, Query, status

from app.api.errors import map_service_error
from app.models.common import PaginatedResponse
from app.models.organization import Organization, OrganizationCreate, OrganizationUpdate
from app.services.errors import ServiceError
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
    try:
        return organization_service.get(organization_id)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.patch("/{organization_id}", response_model=Organization)
def update_organization(organization_id: int, payload: OrganizationUpdate) -> Organization:
    try:
        return organization_service.update(organization_id, payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(organization_id: int) -> None:
    try:
        organization_service.delete(organization_id)
    except ServiceError as error:
        raise map_service_error(error) from error
