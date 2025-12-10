from app.core.logging import logger
from app.models.common import PaginatedResponse
from app.models.organization import Organization, OrganizationCreate, OrganizationUpdate
from app.services.database import InMemoryDatabase
from app.services.errors import ConflictError, NotFoundError
from app.services.pagination import paginate


class OrganizationService:
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def list(self, page: int, page_size: int) -> PaginatedResponse[Organization]:
        return paginate(list(self._db.organizations.values()), page, page_size)

    def create(self, payload: OrganizationCreate) -> Organization:
        organization = Organization(id=self._db.next_id("organizations"), **payload.model_dump())
        self._db.organizations[organization.id] = organization
        logger.info("Organization created", extra={"organization_id": organization.id})
        return organization

    def get(self, organization_id: int) -> Organization:
        organization = self._db.organizations.get(organization_id)
        if organization is None:
            raise NotFoundError("Organization not found")
        return organization

    def update(self, organization_id: int, payload: OrganizationUpdate) -> Organization:
        organization = self.get(organization_id)
        updated = organization.model_copy(update=payload.model_dump(exclude_none=True))
        self._db.organizations[organization_id] = updated
        logger.info("Organization updated", extra={"organization_id": organization_id})
        return updated

    def delete(self, organization_id: int) -> None:
        organization = self._db.organizations.get(organization_id)
        if organization is None:
            raise NotFoundError("Organization not found")
        if any(site.organization_id == organization_id for site in self._db.sites.values()):
            raise ConflictError("Organization has related sites")
        if any(role.organization_id == organization_id for role in self._db.roles.values()):
            raise ConflictError("Organization has related roles")
        if any(
            collab.organization_id == organization_id for collab in self._db.collaborators.values()
        ):
            raise ConflictError("Organization has related collaborators")
        del self._db.organizations[organization_id]
        logger.info("Organization deleted", extra={"organization_id": organization_id})
