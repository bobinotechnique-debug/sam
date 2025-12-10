from fastapi.testclient import TestClient

from app.main import app
from app.services.item_service import item_service


client = TestClient(app)


def setup_function() -> None:  # type: ignore[override]
    item_service.reset()


def test_create_and_list_items() -> None:
    response = client.post("/items", json={"name": "Sample", "description": "demo"})

    assert response.status_code == 201
    payload = response.json()
    assert payload["name"] == "Sample"
    assert payload["description"] == "demo"

    list_response = client.get("/items")
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert items[0]["id"] == payload["id"]


def test_get_item_not_found() -> None:
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_update_and_delete_item() -> None:
    created = client.post("/items", json={"name": "Old", "description": "first"}).json()

    update_response = client.put(
        f"/items/{created['id']}",
        json={"name": "New", "description": "changed"},
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["name"] == "New"
    assert updated["description"] == "changed"

    delete_response = client.delete(f"/items/{created['id']}")
    assert delete_response.status_code == 204

    follow_up_response = client.get(f"/items/{created['id']}")
    assert follow_up_response.status_code == 404
