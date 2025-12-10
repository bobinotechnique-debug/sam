from fastapi import APIRouter, Query, status

from app.models.common import PaginatedResponse
from app.models.role import Role, RoleCreate, RoleUpdate
from app.services.registry import role_service

router = APIRouter(prefix="/api/v1/roles", tags=["roles"])


@router.get("", response_model=PaginatedResponse[Role])
def list_roles(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)
) -> PaginatedResponse[Role]:
    return role_service.list(page, page_size)


@router.post("", response_model=Role, status_code=status.HTTP_201_CREATED)
def create_role(payload: RoleCreate) -> Role:
    return role_service.create(payload)


@router.get("/{role_id}", response_model=Role)
def get_role(role_id: int) -> Role:
    return role_service.get(role_id)


@router.patch("/{role_id}", response_model=Role)
def update_role(role_id: int, payload: RoleUpdate) -> Role:
    return role_service.update(role_id, payload)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int) -> None:
    role_service.delete(role_id)
