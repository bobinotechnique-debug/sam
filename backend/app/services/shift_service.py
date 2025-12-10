from datetime import datetime

from app.core.logging import logger
from app.models.common import PaginatedResponse
from app.models.shift import Shift, ShiftCreate, ShiftUpdate
from app.services.database import InMemoryDatabase
from app.services.errors import ConflictError, NotFoundError, ValidationError
from app.services.pagination import paginate


def _overlaps(start_a: datetime, end_a: datetime, start_b: datetime, end_b: datetime) -> bool:
    return start_a < end_b and start_b < end_a


class ShiftService:
    def __init__(self, db: InMemoryDatabase) -> None:
        self._db = db

    def list(self, page: int, page_size: int) -> PaginatedResponse[Shift]:
        return paginate(list(self._db.shifts.values()), page, page_size)

    def create(self, payload: ShiftCreate) -> Shift:
        mission = self._db.missions.get(payload.mission_id)
        collaborator = self._db.collaborators.get(payload.collaborator_id)
        if mission is None:
            raise NotFoundError("Mission not found")
        if collaborator is None:
            raise NotFoundError("Collaborator not found")
        site = self._db.sites.get(mission.site_id)
        role = self._db.roles.get(mission.role_id)
        if site is None or role is None:
            raise ValidationError("Mission relationships are invalid")
        if collaborator.organization_id != site.organization_id:
            raise ValidationError("Collaborator must belong to the mission organization")
        if collaborator.primary_role_id not in (None, mission.role_id):
            raise ValidationError("Collaborator primary role must match mission role")
        self._assert_no_overlap(collaborator.id, payload.start_utc, payload.end_utc, ignore_id=None)
        shift = Shift(id=self._db.next_id("shifts"), **payload.model_dump())
        self._db.shifts[shift.id] = shift
        logger.info(
            "Shift created",
            extra={
                "shift_id": shift.id,
                "mission_id": payload.mission_id,
                "collaborator_id": payload.collaborator_id,
            },
        )
        return shift

    def get(self, shift_id: int) -> Shift:
        shift = self._db.shifts.get(shift_id)
        if shift is None:
            raise NotFoundError("Shift not found")
        return shift

    def update(self, shift_id: int, payload: ShiftUpdate) -> Shift:
        existing = self.get(shift_id)
        updates = payload.model_dump(exclude_none=True)
        mission_id = updates.get("mission_id", existing.mission_id)
        collaborator_id = updates.get("collaborator_id", existing.collaborator_id)
        mission = self._db.missions.get(mission_id)
        collaborator = self._db.collaborators.get(collaborator_id)
        if mission is None:
            raise NotFoundError("Mission not found")
        if collaborator is None:
            raise NotFoundError("Collaborator not found")
        site = self._db.sites.get(mission.site_id)
        role = self._db.roles.get(mission.role_id)
        if site is None or role is None:
            raise ValidationError("Mission relationships are invalid")
        if collaborator.organization_id != site.organization_id:
            raise ValidationError("Collaborator must belong to the mission organization")
        if collaborator.primary_role_id not in (None, mission.role_id):
            raise ValidationError("Collaborator primary role must match mission role")
        start_utc = updates.get("start_utc", existing.start_utc)
        end_utc = updates.get("end_utc", existing.end_utc)
        self._assert_no_overlap(collaborator_id, start_utc, end_utc, ignore_id=shift_id)
        updated = existing.model_copy(update=updates)
        self._db.shifts[shift_id] = updated
        logger.info("Shift updated", extra={"shift_id": shift_id})
        return updated

    def delete(self, shift_id: int) -> None:
        shift = self._db.shifts.get(shift_id)
        if shift is None:
            raise NotFoundError("Shift not found")
        del self._db.shifts[shift_id]
        logger.info("Shift deleted", extra={"shift_id": shift_id})

    def _assert_no_overlap(
        self, collaborator_id: int, start: datetime, end: datetime, ignore_id: int | None
    ) -> None:
        for shift in self._db.shifts.values():
            if shift.collaborator_id != collaborator_id:
                continue
            if ignore_id is not None and shift.id == ignore_id:
                continue
            if shift.status == "cancelled":
                continue
            if _overlaps(start, end, shift.start_utc, shift.end_utc):
                raise ConflictError("Shift overlaps with an existing assignment")
