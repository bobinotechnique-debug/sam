from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import planning as db_models


def _setup_org_role_site(
    session: Session,
) -> tuple[db_models.Organization, db_models.Role, db_models.Site]:
    org = db_models.Organization(name="Org", timezone="UTC", currency="EUR")
    session.add(org)
    session.flush()
    role = db_models.Role(name="Tech", organization_id=org.id)
    site = db_models.Site(name="HQ", organization_id=org.id, address="", timezone="UTC")
    session.add_all([role, site])
    session.commit()
    session.refresh(role)
    session.refresh(site)
    return org, role, site


def _create_collaborator(
    session: Session, org: db_models.Organization, role: db_models.Role
) -> db_models.Collaborator:
    user = db_models.User(email="alice@example.com", full_name="Alice")
    session.add(user)
    session.flush()
    collaborator = db_models.Collaborator(
        user_id=user.id,
        organization_id=org.id,
        primary_role_id=role.id,
        status="active",
    )
    session.add(collaborator)
    session.commit()
    session.refresh(collaborator)
    return collaborator


def _create_mission(
    session: Session, site_id: int, role_id: int, start: datetime
) -> db_models.Mission:
    site = session.get(db_models.Site, site_id)
    mission = db_models.Mission(
        organization_id=site.organization_id if site else 1,
        site_id=site_id,
        role_id=role_id,
        status="draft",
        title="Mission",
        start_utc=start,
        end_utc=start + timedelta(hours=4),
    )
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


def test_double_booking_detected_in_assignment_conflicts(
    client: TestClient, session: Session
) -> None:
    org, role, site = _setup_org_role_site(session)
    collaborator = _create_collaborator(session, org, role)
    mission_start = datetime.now(UTC)
    mission = _create_mission(session, site.id, role.id, mission_start)

    response_one = client.post(
        "/api/v1/planning/shifts",
        json={
            "mission_id": mission.id,
            "template_id": None,
            "site_id": site.id,
            "role_id": role.id,
            "team_id": None,
            "start_utc": mission_start.isoformat(),
            "end_utc": (mission_start + timedelta(hours=2)).isoformat(),
            "status": "draft",
            "source": "manual",
            "capacity": 1,
        },
    )
    assert response_one.status_code == 201, response_one.text
    shift_one = response_one.json()["shift"]

    response_two = client.post(
        "/api/v1/planning/shifts",
        json={
            "mission_id": mission.id,
            "template_id": None,
            "site_id": site.id,
            "role_id": role.id,
            "team_id": None,
            "start_utc": mission_start.isoformat(),
            "end_utc": (mission_start + timedelta(hours=3)).isoformat(),
            "status": "draft",
            "source": "manual",
            "capacity": 1,
        },
    )
    assert response_two.status_code == 201, response_two.text
    shift_two = response_two.json()["shift"]

    first_assignment = client.post(
        "/api/v1/planning/assignments",
        json={
            "shift_instance_id": shift_one["id"],
            "collaborator_id": collaborator.id,
            "role_id": role.id,
            "status": "confirmed",
            "source": "manual",
        },
    )
    assert first_assignment.status_code == 201

    second_assignment = client.post(
        "/api/v1/planning/assignments",
        json={
            "shift_instance_id": shift_two["id"],
            "collaborator_id": collaborator.id,
            "role_id": role.id,
            "status": "confirmed",
            "source": "manual",
        },
    )
    payload = second_assignment.json()
    assert any(
        conflict["rule"] == "double_booking"
        and conflict["type"] == "hard"
        for conflict in payload["conflicts"]
    )


def test_shift_status_validation(client: TestClient, session: Session) -> None:
    _, role, site = _setup_org_role_site(session)
    mission = _create_mission(session, site.id, role.id, datetime.now(UTC))

    invalid_shift = client.post(
        "/api/v1/planning/shifts",
        json={
            "mission_id": mission.id,
            "template_id": None,
            "site_id": site.id,
            "role_id": role.id,
            "team_id": None,
            "start_utc": mission.start_utc.isoformat(),
            "end_utc": mission.end_utc.isoformat(),
            "status": "invalid_status",
            "source": "manual",
            "capacity": 1,
        },
    )
    assert invalid_shift.status_code == 422


def test_publish_creates_audit_entry(client: TestClient, session: Session) -> None:
    session.add(db_models.Organization(id=1, name="Org", timezone="UTC", currency="EUR"))
    session.commit()

    response = client.post("/api/v1/planning/publish", json={"message": "Go"})
    assert response.status_code == 200

    audit = client.get("/api/v1/planning/audit")
    assert audit.status_code == 200
    assert any(entry["action"] == "publish_planning" for entry in audit.json())
