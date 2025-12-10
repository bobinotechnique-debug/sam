from collections import defaultdict

from app.models.collaborator import Collaborator
from app.models.mission import Mission
from app.models.organization import Organization
from app.models.role import Role
from app.models.shift import Shift
from app.models.site import Site
from app.models.planning_pro import (
    Assignment,
    ConflictRule,
    HrRule,
    Publication,
    ShiftInstance,
    ShiftTemplate,
    UserAvailability,
)


class InMemoryDatabase:
    def __init__(self) -> None:
        self._counters: defaultdict[str, int] = defaultdict(int)
        self.organizations: dict[int, Organization] = {}
        self.sites: dict[int, Site] = {}
        self.roles: dict[int, Role] = {}
        self.collaborators: dict[int, Collaborator] = {}
        self.missions: dict[int, Mission] = {}
        self.shifts: dict[int, Shift] = {}
        self.shift_templates: dict[int, ShiftTemplate] = {}
        self.shift_instances: dict[int, ShiftInstance] = {}
        self.assignments: dict[int, Assignment] = {}
        self.user_availabilities: dict[int, UserAvailability] = {}
        self.hr_rules: dict[int, HrRule] = {}
        self.conflict_rules: dict[int, ConflictRule] = {}
        self.planning_changes: list[dict] = []
        self.publications: dict[int, Publication] = {}
        self.notification_events: dict[int, dict] = {}
        self.auto_assign_jobs: dict[str, dict] = {}

    def next_id(self, key: str) -> int:
        self._counters[key] += 1
        return self._counters[key]

    def reset(self) -> None:
        self._counters.clear()
        self.organizations.clear()
        self.sites.clear()
        self.roles.clear()
        self.collaborators.clear()
        self.missions.clear()
        self.shifts.clear()
        self.shift_templates.clear()
        self.shift_instances.clear()
        self.assignments.clear()
        self.user_availabilities.clear()
        self.hr_rules.clear()
        self.conflict_rules.clear()
        self.planning_changes.clear()
        self.publications.clear()
        self.notification_events.clear()
        self.auto_assign_jobs.clear()
