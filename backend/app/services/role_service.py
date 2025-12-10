from app.models.common import PaginatedResponse
from app.models.role import Role, RoleCreate, RoleUpdate
from app.services.database import InMemoryDatabase
from app.services.errors import ConflictError, NotFoundError
from app.services.pagination import paginate


class RoleService:
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def list(self, page: int, page_size: int) -> PaginatedResponse[Role]:
        return paginate(list(self._db.roles.values()), page, page_size)

    def create(self, payload: RoleCreate) -> Role:
        if payload.organization_id not in self._db.organizations:
            raise NotFoundError("Organization not found")
        role = Role(id=self._db.next_id("roles"), **payload.model_dump())
        self._db.roles[role.id] = role
        return role

    def get(self, role_id: int) -> Role:
        role = self._db.roles.get(role_id)
        if role is None:
            raise NotFoundError("Role not found")
        return role

    def update(self, role_id: int, payload: RoleUpdate) -> Role:
        role = self.get(role_id)
        updated = role.model_copy(update=payload.model_dump(exclude_none=True))
        self._db.roles[role_id] = updated
        return updated

    def delete(self, role_id: int) -> None:
        role = self._db.roles.get(role_id)
        if role is None:
            raise NotFoundError("Role not found")
        if any(collab.primary_role_id == role_id for collab in self._db.collaborators.values()):
            raise ConflictError("Role is assigned to collaborators")
        if any(mission.role_id == role_id for mission in self._db.missions.values()):
            raise ConflictError("Role is used by missions")
        del self._db.roles[role_id]
