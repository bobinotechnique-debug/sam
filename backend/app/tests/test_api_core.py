from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient


def test_organization_crud_flow(client: TestClient) -> None:
    created = client.post(
        "/api/v1/organizations",
        json={
            "name": "Test Org",
            "timezone": "UTC",
            "currency": "EUR",
            "contact_email": "ops@test.org",
        },
    )
    assert created.status_code == 201
    organization_id = created.json()["id"]

    listed = client.get("/api/v1/organizations")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    retrieved = client.get(f"/api/v1/organizations/{organization_id}")
    assert retrieved.status_code == 200
    assert retrieved.json()["name"] == "Test Org"

    updated = client.patch(
        f"/api/v1/organizations/{organization_id}",
        json={"currency": "USD", "timezone": "Europe/Paris"},
    )
    assert updated.status_code == 200
    assert updated.json()["currency"] == "USD"

    deleted = client.delete(f"/api/v1/organizations/{organization_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/organizations/{organization_id}").status_code == 404


def test_role_and_collaborator_validation(client: TestClient) -> None:
    org_a = client.post(
        "/api/v1/organizations", json={"name": "Org A", "timezone": "UTC", "currency": "EUR"}
    ).json()
    org_b = client.post(
        "/api/v1/organizations", json={"name": "Org B", "timezone": "UTC", "currency": "EUR"}
    ).json()

    role_b = client.post(
        "/api/v1/roles",
        json={"organization_id": org_b["id"], "name": "External"},
    ).json()

    invalid_collaborator = client.post(
        "/api/v1/collaborators",
        json={"organization_id": org_a["id"], "full_name": "Bob", "primary_role_id": role_b["id"]},
    )
    assert invalid_collaborator.status_code == 400

    valid_role = client.post(
        "/api/v1/roles",
        json={"organization_id": org_a["id"], "name": "Staff"},
    ).json()

    collaborator = client.post(
        "/api/v1/collaborators",
        json={
            "organization_id": org_a["id"],
            "full_name": "Bob",
            "primary_role_id": valid_role["id"],
        },
    )
    assert collaborator.status_code == 201


def test_mission_requires_matching_organization(client: TestClient) -> None:
    org_primary = client.post(
        "/api/v1/organizations", json={"name": "Org One", "timezone": "UTC", "currency": "EUR"}
    ).json()
    org_other = client.post(
        "/api/v1/organizations", json={"name": "Org Two", "timezone": "UTC", "currency": "EUR"}
    ).json()

    site = client.post(
        "/api/v1/sites",
        json={"organization_id": org_primary["id"], "name": "Main", "timezone": "UTC"},
    ).json()
    other_role = client.post(
        "/api/v1/roles", json={"organization_id": org_other["id"], "name": "Other"}
    ).json()

    invalid_mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site["id"],
            "role_id": other_role["id"],
            "status": "draft",
            "start_utc": datetime.now(UTC).isoformat(),
            "end_utc": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
        },
    )
    assert invalid_mission.status_code == 400

    role = client.post(
        "/api/v1/roles", json={"organization_id": org_primary["id"], "name": "Staff"}
    ).json()

    mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site["id"],
            "role_id": role["id"],
            "status": "draft",
            "start_utc": datetime.now(UTC).isoformat(),
            "end_utc": (datetime.now(UTC) + timedelta(hours=4)).isoformat(),
        },
    )
    assert mission.status_code == 201


def test_shift_crud_flow(client: TestClient) -> None:
    org = client.post(
        "/api/v1/organizations", json={"name": "Org", "timezone": "UTC", "currency": "EUR"}
    ).json()
    role = client.post(
        "/api/v1/roles", json={"organization_id": org["id"], "name": "Role"}
    ).json()
    site = client.post(
        "/api/v1/sites", json={"organization_id": org["id"], "name": "Site", "timezone": "UTC"}
    ).json()
    collaborator = client.post(
        "/api/v1/collaborators",
        json={"organization_id": org["id"], "full_name": "Alice", "primary_role_id": role["id"]},
    ).json()

    start = datetime.now(UTC)
    mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site["id"],
            "role_id": role["id"],
            "status": "draft",
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=3)).isoformat(),
        },
    ).json()

    created_shift = client.post(
        "/api/v1/shifts",
        json={
            "mission_id": mission["id"],
            "collaborator_id": collaborator["id"],
            "status": "confirmed",
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=1)).isoformat(),
        },
    )
    assert created_shift.status_code == 201
    shift_id = created_shift.json()["id"]

    listed = client.get("/api/v1/shifts")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    updated = client.patch(
        f"/api/v1/shifts/{shift_id}",
        json={"status": "cancelled", "cancellation_reason": "Client request"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "cancelled"
    assert updated.json()["cancellation_reason"] == "Client request"

    delete_response = client.delete(f"/api/v1/shifts/{shift_id}")
    assert delete_response.status_code == 204
    assert client.get(f"/api/v1/shifts/{shift_id}").status_code == 404
