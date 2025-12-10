from app.services.collaborator_service import CollaboratorService
from app.services.database import InMemoryDatabase
from app.services.mission_service import MissionService
from app.services.organization_service import OrganizationService
from app.services.role_service import RoleService
from app.services.shift_service import ShiftService
from app.services.site_service import SiteService

db = InMemoryDatabase()
organization_service = OrganizationService(db)
site_service = SiteService(db)
role_service = RoleService(db)
collaborator_service = CollaboratorService(db)
mission_service = MissionService(db)
shift_service = ShiftService(db)
