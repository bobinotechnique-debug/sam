from app.models.common import PaginatedResponse
from app.models.site import Site, SiteCreate, SiteUpdate
from app.services.database import InMemoryDatabase
from app.services.errors import ConflictError, NotFoundError
from app.services.pagination import paginate


class SiteService:
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def list(self, page: int, page_size: int) -> PaginatedResponse[Site]:
        return paginate(list(self._db.sites.values()), page, page_size)

    def create(self, payload: SiteCreate) -> Site:
        organization = self._db.organizations.get(payload.organization_id)
        if organization is None:
            raise NotFoundError("Organization not found")
        timezone = payload.timezone or organization.timezone
        site_data = payload.model_dump()
        site_data["timezone"] = timezone
        site = Site(id=self._db.next_id("sites"), **site_data)
        self._db.sites[site.id] = site
        return site

    def get(self, site_id: int) -> Site:
        site = self._db.sites.get(site_id)
        if site is None:
            raise NotFoundError("Site not found")
        return site

    def update(self, site_id: int, payload: SiteUpdate) -> Site:
        site = self.get(site_id)
        updates = payload.model_dump(exclude_none=True)
        if "timezone" in updates and updates["timezone"] is None:
            updates["timezone"] = site.timezone
        updated = site.model_copy(update=updates)
        self._db.sites[site_id] = updated
        return updated

    def delete(self, site_id: int) -> None:
        site = self._db.sites.get(site_id)
        if site is None:
            raise NotFoundError("Site not found")
        if any(mission.site_id == site_id for mission in self._db.missions.values()):
            raise ConflictError("Site has related missions")
        del self._db.sites[site_id]
