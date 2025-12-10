from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient


def test_healthcheck_returns_details(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert "version" in payload
    assert payload["dependencies"] == {"database": "ok"}
    assert payload["counts"] == {
        "organizations": 0,
        "sites": 0,
        "roles": 0,
        "collaborators": 0,
        "missions": 0,
        "shifts": 0,
    }


def test_metrics_format(client: TestClient) -> None:
    response = client.get("/api/v1/health/metrics")
    assert response.status_code == 200
    assert "codex_entities_total" in response.text
    assert "codex_app_info" in response.text


def test_root_endpoint_gives_navigation(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Backend API is running.",
        "docs_url": "/docs",
        "health_url": "/api/v1/health",
    }


def test_create_organization_and_site_inherits_timezone(client: TestClient) -> None:
    organization = client.post(
        "/api/v1/organizations",
        json={"name": "Acme Corp", "timezone": "Europe/Paris", "currency": "EUR"},
    )
    assert organization.status_code == 201
    org_body = organization.json()

    site = client.post(
        "/api/v1/sites",
        json={"organization_id": org_body["id"], "name": "HQ", "address": "1 rue de Paris"},
    )
    assert site.status_code == 201
    assert site.json()["timezone"] == "Europe/Paris"


def test_shift_overlap_is_rejected(client: TestClient) -> None:
    org = client.post(
        "/api/v1/organizations",
        json={"name": "Overlap Org", "timezone": "UTC", "currency": "EUR"},
    ).json()
    role = client.post(
        "/api/v1/roles", json={"organization_id": org["id"], "name": "Manager"}
    ).json()
    collaborator = client.post(
        "/api/v1/collaborators",
        json={
            "organization_id": org["id"],
            "full_name": "Jane Doe",
            "primary_role_id": role["id"],
        },
    ).json()
    site = client.post(
        "/api/v1/sites", json={"organization_id": org["id"], "name": "Site A", "timezone": "UTC"}
    ).json()
    start = datetime.now(UTC)
    mission = client.post(
        "/api/v1/missions",
        json={
            "site_id": site["id"],
            "role_id": role["id"],
            "status": "draft",
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=4)).isoformat(),
        },
    ).json()
    first_shift = client.post(
        "/api/v1/shifts",
        json={
            "mission_id": mission["id"],
            "collaborator_id": collaborator["id"],
            "start_utc": start.isoformat(),
            "end_utc": (start + timedelta(hours=2)).isoformat(),
            "status": "confirmed",
        },
    )
    assert first_shift.status_code == 201

    overlapping_shift = client.post(
        "/api/v1/shifts",
        json={
            "mission_id": mission["id"],
            "collaborator_id": collaborator["id"],
            "start_utc": (start + timedelta(minutes=30)).isoformat(),
            "end_utc": (start + timedelta(hours=3)).isoformat(),
            "status": "confirmed",
        },
    )
    assert overlapping_shift.status_code == 409
