from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.testclient import TestClient


def _setup_org_role_site(
    client: TestClient,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    org = client.post(
        "/api/v1/organizations",
        json={"name": "Org", "timezone": "UTC", "currency": "EUR"},
    ).json()
    role = client.post(
        "/api/v1/roles",
        json={"organization_id": org["id"], "name": "Tech"},
    ).json()
    site = client.post(
        "/api/v1/sites",
        json={"organization_id": org["id"], "name": "HQ", "address": "", "timezone": None},
    ).json()
    return org, role, site


def _create_collaborator(
    client: TestClient, org: dict[str, Any], role: dict[str, Any]
) -> dict[str, Any]:
    return client.post(
        "/api/v1/collaborators",
        json={
            "organization_id": org["id"],
            "full_name": "Alice",
            "primary_role_id": role["id"],
            "status": "active",
            "email": "alice@example.com",
        },
    ).json()


def _create_mission(
    client: TestClient, site_id: int, role_id: int, start: datetime
) -> dict[str, Any]:
    return client.post(
        "/api/v1/missions",
        json={
            "site_id": site_id,
            "role_id": role_id,
            "status": "draft",
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=4)).isoformat(),
        },
    ).json()


def test_double_booking_detected_in_assignment_conflicts(client: TestClient) -> None:
    org, role, site = _setup_org_role_site(client)
    collaborator = _create_collaborator(client, org, role)
    mission = _create_mission(client, site["id"], role["id"], datetime.now(UTC))
    mission_start = datetime.fromisoformat(mission["start_utc"])

    shift_one = client.post(
        "/api/v1/planning/shifts",
        json={
            "mission_id": mission["id"],
            "template_id": None,
            "site_id": site["id"],
            "role_id": role["id"],
            "team_id": None,
            "start_utc": mission["start_utc"],
            "end_utc": (mission_start + timedelta(hours=2)).isoformat(),
            "status": "draft",
            "source": "manual",
            "capacity": 1,
        },
    ).json()["shift"]

    shift_two = client.post(
        "/api/v1/planning/shifts",
        json={
            "mission_id": mission["id"],
            "template_id": None,
            "site_id": site["id"],
            "role_id": role["id"],
            "team_id": None,
            "start_utc": mission["start_utc"],
            "end_utc": (mission_start + timedelta(hours=3)).isoformat(),
            "status": "draft",
            "source": "manual",
            "capacity": 1,
        },
    ).json()["shift"]

    first_assignment = client.post(
        "/api/v1/planning/assignments",
        json={
            "shift_instance_id": shift_one["id"],
            "collaborator_id": collaborator["id"],
            "role_id": role["id"],
            "status": "confirmed",
            "source": "manual",
        },
    )
    assert first_assignment.status_code == 201

    second_assignment = client.post(
        "/api/v1/planning/assignments",
        json={
            "shift_instance_id": shift_two["id"],
            "collaborator_id": collaborator["id"],
            "role_id": role["id"],
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


def test_shift_status_validation(client: TestClient) -> None:
    _, role, site = _setup_org_role_site(client)
    mission = _create_mission(client, site["id"], role["id"], datetime.now(UTC))

    invalid_shift = client.post(
        "/api/v1/planning/shifts",
        json={
            "mission_id": mission["id"],
            "template_id": None,
            "site_id": site["id"],
            "role_id": role["id"],
            "team_id": None,
            "start_utc": mission["start_utc"],
            "end_utc": mission["end_utc"],
            "status": "invalid_status",
            "source": "manual",
            "capacity": 1,
        },
    )
    assert invalid_shift.status_code == 422


def test_publish_creates_audit_entry(client: TestClient) -> None:
    response = client.post("/api/v1/planning/publish", json={"message": "Go"})
    assert response.status_code == 200

    audit = client.get("/api/v1/planning/audit")
    assert audit.status_code == 200
    assert any(entry["action"] == "publish_planning" for entry in audit.json())
