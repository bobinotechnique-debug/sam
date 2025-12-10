from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="EUR", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sites: Mapped[list[Site]] = relationship(back_populates="organization")
    teams: Mapped[list[Team]] = relationship(back_populates="organization")
    roles: Mapped[list[Role]] = relationship(back_populates="organization")
    skills: Mapped[list[Skill]] = relationship(back_populates="organization")
    collaborators: Mapped[list[Collaborator]] = relationship(back_populates="organization")
    missions: Mapped[list[Mission]] = relationship(back_populates="organization")
    hr_rules: Mapped[list[HrRule]] = relationship(back_populates="organization")
    conflict_rules: Mapped[list[ConflictRule]] = relationship(back_populates="organization")


class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", nullable=False)
    address: Mapped[str | None] = mapped_column(String(255))

    organization: Mapped[Organization] = relationship(back_populates="sites")
    teams: Mapped[list[Team]] = relationship(back_populates="site")
    missions: Mapped[list[Mission]] = relationship(back_populates="site")
    blackouts: Mapped[list[Blackout]] = relationship(back_populates="site")


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    site_id: Mapped[int | None] = mapped_column(ForeignKey("sites.id"))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    color_hex: Mapped[str | None] = mapped_column(String(7))

    organization: Mapped[Organization] = relationship(back_populates="teams")
    site: Mapped[Site | None] = relationship(back_populates="teams")
    missions: Mapped[list[Mission]] = relationship(back_populates="team")
    shift_templates: Mapped[list[ShiftTemplate]] = relationship(back_populates="team")
    shift_instances: Mapped[list[ShiftInstance]] = relationship(back_populates="team")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    organization: Mapped[Organization] = relationship(back_populates="roles")
    skills: Mapped[list[RoleSkill]] = relationship(back_populates="role")
    missions: Mapped[list[Mission]] = relationship(back_populates="role")
    shift_templates: Mapped[list[ShiftTemplate]] = relationship(back_populates="role")
    shift_instances: Mapped[list[ShiftInstance]] = relationship(back_populates="role")
    assignments: Mapped[list[Assignment]] = relationship(back_populates="role")


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    organization: Mapped[Organization] = relationship(back_populates="skills")
    roles: Mapped[list[RoleSkill]] = relationship(back_populates="skill")
    collaborators: Mapped[list[CollaboratorSkill]] = relationship(back_populates="skill")


class RoleSkill(Base):
    __tablename__ = "role_skills"
    __table_args__ = (UniqueConstraint("role_id", "skill_id", name="uix_role_skill"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)

    role: Mapped[Role] = relationship(back_populates="skills")
    skill: Mapped[Skill] = relationship(back_populates="roles")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    collaborator: Mapped[Collaborator | None] = relationship(back_populates="user")
    authored_publications: Mapped[list[Publication]] = relationship(
        back_populates="author", foreign_keys="Publication.author_user_id"
    )
    notification_events: Mapped[list[NotificationEvent]] = relationship(
        back_populates="recipient", foreign_keys="NotificationEvent.recipient_user_id"
    )


class Collaborator(Base):
    __tablename__ = "collaborators"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    primary_role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))
    status: Mapped[str] = mapped_column(String(50), default="active")

    user: Mapped[User] = relationship(back_populates="collaborator")
    organization: Mapped[Organization] = relationship(back_populates="collaborators")
    primary_role: Mapped[Role | None] = relationship()
    skills: Mapped[list[CollaboratorSkill]] = relationship(back_populates="collaborator")
    assignments: Mapped[list[Assignment]] = relationship(back_populates="collaborator")
    availabilities: Mapped[list[UserAvailability]] = relationship(back_populates="collaborator")
    leaves: Mapped[list[Leave]] = relationship(back_populates="collaborator")


class CollaboratorSkill(Base):
    __tablename__ = "collaborator_skills"
    __table_args__ = (UniqueConstraint("collaborator_id", "skill_id", name="uix_collab_skill"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    collaborator_id: Mapped[int] = mapped_column(ForeignKey("collaborators.id"), nullable=False)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)

    collaborator: Mapped[Collaborator] = relationship(back_populates="skills")
    skill: Mapped[Skill] = relationship(back_populates="collaborators")


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    start_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    budget_target: Mapped[float | None] = mapped_column(Float)
    note: Mapped[str | None] = mapped_column(Text())

    organization: Mapped[Organization] = relationship(back_populates="missions")
    site: Mapped[Site] = relationship(back_populates="missions")
    role: Mapped[Role] = relationship(back_populates="missions")
    team: Mapped[Team | None] = relationship(back_populates="missions")
    shift_templates: Mapped[list[ShiftTemplate]] = relationship(back_populates="mission")
    shift_instances: Mapped[list[ShiftInstance]] = relationship(back_populates="mission")


class ShiftTemplate(Base):
    __tablename__ = "shift_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    mission_id: Mapped[int] = mapped_column(ForeignKey("missions.id"), nullable=False)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    recurrence_rule: Mapped[str | None] = mapped_column(String(255))
    start_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expected_headcount: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    mission: Mapped[Mission] = relationship(back_populates="shift_templates")
    site: Mapped[Site] = relationship()
    role: Mapped[Role] = relationship(back_populates="shift_templates")
    team: Mapped[Team | None] = relationship(back_populates="shift_templates")
    shift_instances: Mapped[list[ShiftInstance]] = relationship(back_populates="template")

    __table_args__ = (
        CheckConstraint("start_time_utc < end_time_utc", name="ck_template_time_order"),
    )


class ShiftInstance(Base):
    __tablename__ = "shift_instances"

    id: Mapped[int] = mapped_column(primary_key=True)
    mission_id: Mapped[int] = mapped_column(ForeignKey("missions.id"), nullable=False)
    template_id: Mapped[int | None] = mapped_column(ForeignKey("shift_templates.id"))
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    start_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    source: Mapped[str] = mapped_column(String(50), default="manual", nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, default=1)

    mission: Mapped[Mission] = relationship(back_populates="shift_instances")
    template: Mapped[ShiftTemplate | None] = relationship(back_populates="shift_instances")
    site: Mapped[Site] = relationship()
    role: Mapped[Role] = relationship(back_populates="shift_instances")
    team: Mapped[Team | None] = relationship(back_populates="shift_instances")
    assignments: Mapped[list[Assignment]] = relationship(back_populates="shift_instance")

    __table_args__ = (
        CheckConstraint("start_utc < end_utc", name="ck_shift_instance_time_order"),
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    shift_instance_id: Mapped[int] = mapped_column(ForeignKey("shift_instances.id"), nullable=False)
    collaborator_id: Mapped[int] = mapped_column(ForeignKey("collaborators.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="proposed", nullable=False)
    source: Mapped[str] = mapped_column(String(50), default="manual", nullable=False)
    note: Mapped[str | None] = mapped_column(Text())
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    shift_instance: Mapped[ShiftInstance] = relationship(back_populates="assignments")
    collaborator: Mapped[Collaborator] = relationship(back_populates="assignments")
    role: Mapped[Role] = relationship(back_populates="assignments")


class UserAvailability(Base):
    __tablename__ = "user_availabilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    collaborator_id: Mapped[int] = mapped_column(ForeignKey("collaborators.id"), nullable=False)
    start_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    reason: Mapped[str | None] = mapped_column(String(255))

    collaborator: Mapped[Collaborator] = relationship(back_populates="availabilities")

    __table_args__ = (CheckConstraint("start_utc < end_utc", name="ck_availability_time_order"),)


class Leave(Base):
    __tablename__ = "leaves"

    id: Mapped[int] = mapped_column(primary_key=True)
    collaborator_id: Mapped[int] = mapped_column(ForeignKey("collaborators.id"), nullable=False)
    start_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)

    collaborator: Mapped[Collaborator] = relationship(back_populates="leaves")

    __table_args__ = (CheckConstraint("start_utc < end_utc", name="ck_leave_time_order"),)


class Blackout(Base):
    __tablename__ = "blackouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), nullable=False)
    start_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255))
    is_hard_limit: Mapped[bool] = mapped_column(Boolean, default=True)

    site: Mapped[Site] = relationship(back_populates="blackouts")

    __table_args__ = (CheckConstraint("start_utc < end_utc", name="ck_blackout_time_order"),)


class HrRule(Base):
    __tablename__ = "hr_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="hard", nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    config: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    organization: Mapped[Organization] = relationship(back_populates="hr_rules")


class ConflictRule(Base):
    __tablename__ = "conflict_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="error", nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    config: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    organization: Mapped[Organization] = relationship(back_populates="conflict_rules")


class PlanningChange(Base):
    __tablename__ = "planning_changes"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    organization: Mapped[Organization] = relationship()
    actor: Mapped[User | None] = relationship()


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    author_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(20), default="draft", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    message: Mapped[str | None] = mapped_column(String(255))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    organization: Mapped[Organization] = relationship()
    author: Mapped[User | None] = relationship(back_populates="authored_publications")


class NotificationEvent(Base):
    __tablename__ = "notification_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    recipient_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    related_shift_instance_id: Mapped[int | None] = mapped_column(ForeignKey("shift_instances.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    recipient: Mapped[User | None] = relationship(back_populates="notification_events")
    shift_instance: Mapped[ShiftInstance | None] = relationship()
    organization: Mapped[Organization] = relationship()


__all__ = [
    "Organization",
    "Site",
    "Team",
    "Role",
    "Skill",
    "RoleSkill",
    "User",
    "Collaborator",
    "CollaboratorSkill",
    "Mission",
    "ShiftTemplate",
    "ShiftInstance",
    "Assignment",
    "UserAvailability",
    "Leave",
    "Blackout",
    "HrRule",
    "ConflictRule",
    "PlanningChange",
    "Publication",
    "NotificationEvent",
]
