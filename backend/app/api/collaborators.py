from fastapi import APIRouter, Query, status

from app.api.errors import map_service_error
from app.models.collaborator import Collaborator, CollaboratorCreate, CollaboratorUpdate
from app.models.common import PaginatedResponse
from app.services.errors import ServiceError
from app.services.registry import collaborator_service

router = APIRouter(prefix="/api/v1/collaborators", tags=["collaborators"])


@router.get("", response_model=PaginatedResponse[Collaborator])
def list_collaborators(
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)
) -> PaginatedResponse[Collaborator]:
    return collaborator_service.list(page, page_size)


@router.post("", response_model=Collaborator, status_code=status.HTTP_201_CREATED)
def create_collaborator(payload: CollaboratorCreate) -> Collaborator:
    try:
        return collaborator_service.create(payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.get("/{collaborator_id}", response_model=Collaborator)
def get_collaborator(collaborator_id: int) -> Collaborator:
    try:
        return collaborator_service.get(collaborator_id)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.patch("/{collaborator_id}", response_model=Collaborator)
def update_collaborator(collaborator_id: int, payload: CollaboratorUpdate) -> Collaborator:
    try:
        return collaborator_service.update(collaborator_id, payload)
    except ServiceError as error:
        raise map_service_error(error) from error


@router.delete("/{collaborator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collaborator(collaborator_id: int) -> None:
    try:
        collaborator_service.delete(collaborator_id)
    except ServiceError as error:
        raise map_service_error(error) from error
