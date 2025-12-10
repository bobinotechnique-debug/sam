from app.services.collaborator_service import CollaboratorService
from app.services.database import InMemoryDatabase
from app.services.mission_service import MissionService
from app.services.organization_service import OrganizationService
from app.services.planning_pro import (
    AssignmentService,
    AuditService,
    AutoAssignJobService,
    AvailabilityService,
    PublicationService,
    RuleService,
    ShiftInstanceService,
    ShiftTemplateService,
)
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
rule_service = RuleService(db)
planning_shift_template_service = ShiftTemplateService(db)
planning_shift_instance_service = ShiftInstanceService(db, rule_service)
planning_assignment_service = AssignmentService(db, rule_service)
planning_availability_service = AvailabilityService(db)
planning_audit_service = AuditService(db)
planning_publication_service = PublicationService(db, planning_audit_service)
planning_auto_assign_service = AutoAssignJobService(db, planning_assignment_service)
planning_rule_service = rule_service
