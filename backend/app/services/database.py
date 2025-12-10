from collections import defaultdict

from app.models.collaborator import Collaborator
from app.models.mission import Mission
from app.models.organization import Organization
from app.models.role import Role
from app.models.shift import Shift
from app.models.site import Site


class InMemoryDatabase:
    def __init__(self) -> None:
        self._counters: defaultdict[str, int] = defaultdict(int)
        self.organizations: dict[int, Organization] = {}
        self.sites: dict[int, Site] = {}
        self.roles: dict[int, Role] = {}
        self.collaborators: dict[int, Collaborator] = {}
        self.missions: dict[int, Mission] = {}
        self.shifts: dict[int, Shift] = {}

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
