from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.testclient import TestClient


def _create_org_role_site(
    client: TestClient,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    org = client.post(
        "/api/v1/organizations",
        json={"name": "Org", "timezone": "Europe/Paris", "currency": "EUR"},
    ).json()
    role = client.post(
        "/api/v1/roles", json={"organization_id": org["id"], "name": "Staff"}
    ).json()
    site = client.post(
        "/api/v1/sites",
        json={"organization_id": org["id"], "name": "HQ", "address": "", "timezone": None},
    ).json()
    return org, role, site


def test_site_inherits_organization_timezone_when_not_provided(client: TestClient) -> None:
    org, _, site = _create_org_role_site(client)

    assert site["timezone"] == org["timezone"]


def test_site_deletion_blocked_when_mission_exists(client: TestClient) -> None:
    _, role, site = _create_org_role_site(client)
    start = datetime.now(UTC)
    mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site["id"],
            "role_id": role["id"],
            "status": "draft",
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=2)).isoformat(),
        },
    )
    assert mission.status_code == 201

    delete_response = client.delete(f"/api/v1/sites/{site['id']}")
    assert delete_response.status_code == 409
    assert delete_response.json()["code"] == "conflict"


def test_collaborator_deletion_blocked_when_shift_exists(client: TestClient) -> None:
    org, role, site = _create_org_role_site(client)
    collaborator = client.post(
        "/api/v1/collaborators",
        json={
            "organization_id": org["id"],
            "full_name": "Alice",
            "primary_role_id": role["id"],
            "status": "active",
            "email": "alice@example.com",
        },
    ).json()
    start = datetime.now(UTC)
    mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site["id"],
            "role_id": role["id"],
            "status": "published",
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=3)).isoformat(),
        },
    ).json()
    shift = client.post(
        "/api/v1/shifts",
        json={
            "mission_id": mission["id"],
            "collaborator_id": collaborator["id"],
            "status": "confirmed",
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=1)).isoformat(),
        },
    )
    assert shift.status_code == 201

    delete_response = client.delete(f"/api/v1/collaborators/{collaborator['id']}")
    assert delete_response.status_code == 409
    assert "shifts" in delete_response.json()["message"]


def test_planning_style_mission_update_validates_relationships(client: TestClient) -> None:
    org, role, site = _create_org_role_site(client)
    second_site = client.post(
        "/api/v1/sites",
        json={"organization_id": org["id"], "name": "Satellite", "timezone": "UTC"},
    ).json()
    mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site["id"],
            "role_id": role["id"],
            "status": "draft",
            "start_utc": datetime.now(UTC).isoformat(),
            "end_utc": (datetime.now(UTC) + timedelta(hours=1)).isoformat(),
        },
    ).json()

    updated = client.patch(
        f"/api/v1/missions/{mission['id']}",
        json={
            "site_id": second_site["id"],
            "note": "Replanifié depuis la vue planning",
            "start_utc": datetime.now(UTC).isoformat(),
            "end_utc": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
        },
    )
    assert updated.status_code == 200
    payload = updated.json()
    assert payload["site_id"] == second_site["id"]
    assert payload["note"] == "Replanifié depuis la vue planning"

    other_org = client.post(
        "/api/v1/organizations", json={"name": "Other", "timezone": "UTC", "currency": "EUR"}
    ).json()
    other_role = client.post(
        "/api/v1/roles", json={"organization_id": other_org["id"], "name": "External"}
    ).json()

    invalid_update = client.patch(
        f"/api/v1/missions/{mission['id']}",
        json={"role_id": other_role["id"]},
    )
    assert invalid_update.status_code == 400
    assert "same organization" in invalid_update.json()["message"]
