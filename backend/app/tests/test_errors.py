from fastapi.testclient import TestClient


def test_service_error_response_structure(client: TestClient) -> None:
    response = client.get("/api/v1/organizations/9999")
    assert response.status_code == 404
    payload = response.json()
    assert payload["code"] == "not_found"
    assert payload["message"] == "Organization not found"
    assert payload["trace_id"]
    assert response.headers["X-Request-ID"] == payload["trace_id"]


def test_request_validation_error_response(client: TestClient) -> None:
    response = client.post(
        "/api/v1/organizations",
        json={"name": "", "timezone": "Invalid/Timezone", "currency": "EUR"},
    )
    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "request_validation_error"
    assert payload["trace_id"]
    assert isinstance(payload["detail"], list)
    assert response.headers["X-Request-ID"] == payload["trace_id"]
