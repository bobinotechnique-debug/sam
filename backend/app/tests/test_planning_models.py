from datetime import UTC, datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.models import planning as models


def test_sqlalchemy_models_link_assignments(tmp_path: Path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path}/planning.db")
    Base.metadata.create_all(engine)

    start = datetime.now(UTC)
    end = start + timedelta(hours=4)

    with Session(engine) as session:
        org = models.Organization(name="Acme", timezone="UTC", currency="EUR")
        site = models.Site(organization=org, name="HQ", timezone="UTC")
        role = models.Role(organization=org, name="Technicien")
        user = models.User(email="tech@example.com", full_name="Tech One")
        collaborator = models.Collaborator(user=user, organization=org, status="active")
        mission = models.Mission(
            organization=org,
            site=site,
            role=role,
            title="Mise en place",
            status="draft",
            start_utc=start,
            end_utc=end,
        )
        template = models.ShiftTemplate(
            mission=mission,
            site=site,
            role=role,
            start_time_utc=start,
            end_time_utc=start + timedelta(hours=2),
            expected_headcount=2,
        )
        instance = models.ShiftInstance(
            mission=mission,
            template=template,
            site=site,
            role=role,
            start_utc=start,
            end_utc=start + timedelta(hours=1),
            status="draft",
            source="manual",
        )
        assignment = models.Assignment(
            shift_instance=instance,
            collaborator=collaborator,
            role=role,
            status="proposed",
            source="manual",
        )

        session.add_all([org, site, role, mission, template, instance, assignment])
        session.commit()

        stored_instance = session.get(models.ShiftInstance, instance.id)
        assert stored_instance is not None
        assert stored_instance.assignments[0].collaborator.user.email == "tech@example.com"


def test_rules_defaults_are_persisted(tmp_path: Path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path}/planning.db")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        org = models.Organization(name="Beta", timezone="UTC", currency="EUR")
        hr_rule = models.HrRule(
            organization=org, code="max_hours_week", severity="hard", config={"hours": 40}
        )
        conflict_rule = models.ConflictRule(
            organization=org,
            code="double_booking",
            severity="error",
            config={"enforced": True},
        )
        session.add_all([org, hr_rule, conflict_rule])
        session.commit()

        stored_hr = session.get(models.HrRule, hr_rule.id)
        stored_conflict = session.get(models.ConflictRule, conflict_rule.id)
        assert stored_hr and stored_hr.config["hours"] == 40
        assert stored_conflict and stored_conflict.severity == "error"
