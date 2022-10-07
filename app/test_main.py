from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

# remember: must start all test functions with test_


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get(
        "/items/baz",
        headers={"X-Token": "coneofsilence"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
