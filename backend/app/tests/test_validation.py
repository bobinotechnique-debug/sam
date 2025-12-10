from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient


def _create_org_site_and_role(client: TestClient) -> tuple[int, int, int]:
    org = client.post(
        "/api/v1/organizations",
        json={"name": "Org", "timezone": "UTC", "currency": "EUR"},
    ).json()
    site = client.post(
        "/api/v1/sites",
        json={"organization_id": org["id"], "name": "HQ", "timezone": "UTC"},
    ).json()
    role = client.post(
        "/api/v1/roles",
        json={"organization_id": org["id"], "name": "Operator"},
    ).json()
    return org["id"], site["id"], role["id"]


def test_mission_requires_valid_time_window(client: TestClient) -> None:
    _, site_id, role_id = _create_org_site_and_role(client)
    start = datetime.now(UTC)
    response = client.post(
        "/api/v1/missions",
        json={
            "site_id": site_id,
            "role_id": role_id,
            "status": "draft",
            "start_utc": (start + timedelta(hours=2)).isoformat(),
            "end_utc": (start + timedelta(hours=1)).isoformat(),
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "request_validation_error"


def test_mission_update_validates_site_and_role_organization(client: TestClient) -> None:
    org_primary, site_id, role_id = _create_org_site_and_role(client)
    other_org = client.post(
        "/api/v1/organizations",
        json={"name": "Other", "timezone": "UTC", "currency": "EUR"},
    ).json()
    other_role = client.post(
        "/api/v1/roles",
        json={"organization_id": other_org["id"], "name": "External"},
    ).json()

    mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site_id,
            "role_id": role_id,
            "status": "draft",
            "start_utc": datetime.now(UTC).isoformat(),
            "end_utc": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
        },
    ).json()

    update = client.patch(
        f"/api/v1/missions/{mission['id']}",
        json={"role_id": other_role["id"]},
    )

    assert update.status_code == 400
    payload = update.json()
    assert payload["code"] == "validation_error"
    assert "Role and site must belong to the same organization" in payload["message"]

    # Updating within the same organization succeeds
    second_role = client.post(
        "/api/v1/roles",
        json={"organization_id": org_primary, "name": "Backup"},
    ).json()
    ok_response = client.patch(
        f"/api/v1/missions/{mission['id']}",
        json={"role_id": second_role["id"]},
    )
    assert ok_response.status_code == 200


def test_shift_overlap_is_rejected(client: TestClient) -> None:
    organization_id, site_id, role_id = _create_org_site_and_role(client)
    collaborator = client.post(
        "/api/v1/collaborators",
        json={
            "organization_id": organization_id,
            "full_name": "Alice",
            "primary_role_id": role_id,
            "status": "active",
        },
    ).json()

    start = datetime.now(UTC)
    mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site_id,
            "role_id": role_id,
            "status": "published",
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=3)).isoformat(),
        },
    ).json()

    first_shift = client.post(
        "/api/v1/shifts",
        json={
            "mission_id": mission["id"],
            "collaborator_id": collaborator["id"],
            "status": "confirmed",
            "start_utc": (start + timedelta(minutes=15)).isoformat(),
            "end_utc": (start + timedelta(hours=1)).isoformat(),
        },
    )
    assert first_shift.status_code == 201

    conflict = client.post(
        "/api/v1/shifts",
        json={
            "mission_id": mission["id"],
            "collaborator_id": collaborator["id"],
            "status": "confirmed",
            "start_utc": (start + timedelta(minutes=45)).isoformat(),
            "end_utc": (start + timedelta(hours=1, minutes=30)).isoformat(),
        },
    )

    assert conflict.status_code == 409
    payload = conflict.json()
    assert payload["code"] == "conflict"
    assert "overlaps" in payload["message"]

