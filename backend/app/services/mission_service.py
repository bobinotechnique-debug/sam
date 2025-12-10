from app.models.common import PaginatedResponse
from app.models.mission import Mission, MissionCreate, MissionUpdate
from app.services.database import InMemoryDatabase
from app.services.errors import ConflictError, NotFoundError, ValidationError
from app.services.pagination import paginate


class MissionService:
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def list(self, page: int, page_size: int) -> PaginatedResponse[Mission]:
        return paginate(list(self._db.missions.values()), page, page_size)

    def create(self, payload: MissionCreate) -> Mission:
        site = self._db.sites.get(payload.site_id)
        if site is None:
            raise NotFoundError("Site not found")
        role = self._db.roles.get(payload.role_id)
        if role is None:
            raise NotFoundError("Role not found")
        if role.organization_id != site.organization_id:
            raise ValidationError("Role and site must belong to the same organization")
        mission = Mission(id=self._db.next_id("missions"), **payload.model_dump())
        self._db.missions[mission.id] = mission
        return mission

    def get(self, mission_id: int) -> Mission:
        mission = self._db.missions.get(mission_id)
        if mission is None:
            raise NotFoundError("Mission not found")
        return mission

    def update(self, mission_id: int, payload: MissionUpdate) -> Mission:
        mission = self.get(mission_id)
        updates = payload.model_dump(exclude_none=True)
        if "site_id" in updates:
            site = self._db.sites.get(updates["site_id"])
            if site is None:
                raise NotFoundError("Site not found")
        else:
            site = self._db.sites.get(mission.site_id)
        if "role_id" in updates:
            role = self._db.roles.get(updates["role_id"])
            if role is None:
                raise NotFoundError("Role not found")
        else:
            role = self._db.roles.get(mission.role_id)
        if site is None or role is None:
            raise ValidationError("Mission relationships are invalid")
        if site.organization_id != role.organization_id:
            raise ValidationError("Role and site must belong to the same organization")
        updated = mission.model_copy(update=updates)
        self._db.missions[mission_id] = updated
        return updated

    def delete(self, mission_id: int) -> None:
        mission = self._db.missions.get(mission_id)
        if mission is None:
            raise NotFoundError("Mission not found")
        if any(shift.mission_id == mission_id for shift in self._db.shifts.values()):
            raise ConflictError("Mission has related shifts")
        del self._db.missions[mission_id]
