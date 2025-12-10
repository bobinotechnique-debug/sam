from app.core.logging import logger
from app.models.collaborator import Collaborator, CollaboratorCreate, CollaboratorUpdate
from app.models.common import PaginatedResponse
from app.services.database import InMemoryDatabase
from app.services.errors import ConflictError, NotFoundError, ValidationError
from app.services.pagination import paginate


class CollaboratorService:
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def list(self, page: int, page_size: int) -> PaginatedResponse[Collaborator]:
        return paginate(list(self._db.collaborators.values()), page, page_size)

    def create(self, payload: CollaboratorCreate) -> Collaborator:
        if payload.organization_id not in self._db.organizations:
            raise NotFoundError("Organization not found")
        if payload.primary_role_id is not None:
            role = self._db.roles.get(payload.primary_role_id)
            if role is None:
                raise NotFoundError("Role not found")
            if role.organization_id != payload.organization_id:
                raise ValidationError("Role must belong to the collaborator organization")
        collaborator = Collaborator(id=self._db.next_id("collaborators"), **payload.model_dump())
        self._db.collaborators[collaborator.id] = collaborator
        logger.info(
            "Collaborator created",
            extra={"collaborator_id": collaborator.id, "organization_id": payload.organization_id},
        )
        return collaborator

    def get(self, collaborator_id: int) -> Collaborator:
        collaborator = self._db.collaborators.get(collaborator_id)
        if collaborator is None:
            raise NotFoundError("Collaborator not found")
        return collaborator

    def update(self, collaborator_id: int, payload: CollaboratorUpdate) -> Collaborator:
        collaborator = self.get(collaborator_id)
        updates = payload.model_dump(exclude_none=True)
        if "primary_role_id" in updates and updates["primary_role_id"] is not None:
            role = self._db.roles.get(updates["primary_role_id"])
            if role is None:
                raise NotFoundError("Role not found")
            if role.organization_id != collaborator.organization_id:
                raise ValidationError("Role must belong to the collaborator organization")
        updated = collaborator.model_copy(update=updates)
        self._db.collaborators[collaborator_id] = updated
        logger.info("Collaborator updated", extra={"collaborator_id": collaborator_id})
        return updated

    def delete(self, collaborator_id: int) -> None:
        collaborator = self._db.collaborators.get(collaborator_id)
        if collaborator is None:
            raise NotFoundError("Collaborator not found")
        if any(shift.collaborator_id == collaborator_id for shift in self._db.shifts.values()):
            raise ConflictError("Collaborator is referenced by shifts")
        del self._db.collaborators[collaborator_id]
        logger.info("Collaborator deleted", extra={"collaborator_id": collaborator_id})
