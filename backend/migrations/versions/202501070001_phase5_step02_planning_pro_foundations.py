"""Phase 5 – Step 02 – Planning PRO foundations

Revision ID: 202501070001
Revises: 
Create Date: 2025-01-07 00:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "202501070001"
down_revision = None
branch_labels = None
depends_on = None


# NOTE: This migration sets up the Planning PRO foundations described in
# docs/roadmap/phase5/step-02.md.

def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False, server_default="UTC"),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="EUR"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "sites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False, server_default="UTC"),
        sa.Column("address", sa.String(length=255)),
    )

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id")),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("color_hex", sa.String(length=7)),
    )

    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.String(length=255)),
    )

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False, server_default="UTC"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    op.create_table(
        "missions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id")),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("start_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("budget_target", sa.Float()),
        sa.Column("note", sa.Text()),
        sa.CheckConstraint("start_utc < end_utc", name="ck_mission_time_order"),
    )

    op.create_table(
        "role_skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("skills.id"), nullable=False),
        sa.UniqueConstraint("role_id", "skill_id", name="uix_role_skill"),
    )

    op.create_table(
        "collaborators",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("primary_role_id", sa.Integer(), sa.ForeignKey("roles.id")),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
    )

    op.create_table(
        "collaborator_skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("collaborator_id", sa.Integer(), sa.ForeignKey("collaborators.id"), nullable=False),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("skills.id"), nullable=False),
        sa.UniqueConstraint("collaborator_id", "skill_id", name="uix_collab_skill"),
    )

    op.create_table(
        "shift_templates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mission_id", sa.Integer(), sa.ForeignKey("missions.id"), nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id")),
        sa.Column("recurrence_rule", sa.String(length=255)),
        sa.Column("start_time_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expected_headcount", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")),
        sa.CheckConstraint("start_time_utc < end_time_utc", name="ck_template_time_order"),
    )

    op.create_table(
        "shift_instances",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mission_id", sa.Integer(), sa.ForeignKey("missions.id"), nullable=False),
        sa.Column("template_id", sa.Integer(), sa.ForeignKey("shift_templates.id")),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id")),
        sa.Column("start_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("source", sa.String(length=50), nullable=False, server_default="manual"),
        sa.Column("capacity", sa.Integer(), nullable=False, server_default="1"),
        sa.CheckConstraint("start_utc < end_utc", name="ck_shift_instance_time_order"),
    )

    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shift_instance_id", sa.Integer(), sa.ForeignKey("shift_instances.id"), nullable=False),
        sa.Column("collaborator_id", sa.Integer(), sa.ForeignKey("collaborators.id"), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="proposed"),
        sa.Column("source", sa.String(length=50), nullable=False, server_default="manual"),
        sa.Column("note", sa.Text()),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default=sa.text("FALSE")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "user_availabilities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("collaborator_id", sa.Integer(), sa.ForeignKey("collaborators.id"), nullable=False),
        sa.Column("start_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")),
        sa.Column("reason", sa.String(length=255)),
        sa.CheckConstraint("start_utc < end_utc", name="ck_availability_time_order"),
    )

    op.create_table(
        "leaves",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("collaborator_id", sa.Integer(), sa.ForeignKey("collaborators.id"), nullable=False),
        sa.Column("start_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.CheckConstraint("start_utc < end_utc", name="ck_leave_time_order"),
    )

    op.create_table(
        "blackouts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("sites.id"), nullable=False),
        sa.Column("start_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_utc", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.String(length=255)),
        sa.Column("is_hard_limit", sa.Boolean(), nullable=False, server_default=sa.text("TRUE")),
        sa.CheckConstraint("start_utc < end_utc", name="ck_blackout_time_order"),
    )

    op.create_table(
        "hr_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("code", sa.String(length=120), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False, server_default="hard"),
        sa.Column("description", sa.String(length=255)),
        sa.Column("config", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )

    op.create_table(
        "conflict_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("code", sa.String(length=120), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False, server_default="error"),
        sa.Column("description", sa.String(length=255)),
        sa.Column("config", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
    )

    op.create_table(
        "planning_changes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "publications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("author_user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("message", sa.String(length=255)),
        sa.Column("published_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "notification_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization_id", sa.Integer(), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("recipient_user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("related_shift_instance_id", sa.Integer(), sa.ForeignKey("shift_instances.id")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("read_at", sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table("notification_events")
    op.drop_table("publications")
    op.drop_table("planning_changes")
    op.drop_table("conflict_rules")
    op.drop_table("hr_rules")
    op.drop_table("blackouts")
    op.drop_table("leaves")
    op.drop_table("user_availabilities")
    op.drop_table("assignments")
    op.drop_table("shift_instances")
    op.drop_table("shift_templates")
    op.drop_table("collaborator_skills")
    op.drop_table("collaborators")
    op.drop_table("role_skills")
    op.drop_table("missions")
    op.drop_table("users")
    op.drop_table("skills")
    op.drop_table("roles")
    op.drop_table("teams")
    op.drop_table("sites")
    op.drop_table("organizations")
