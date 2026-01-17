from fastapi.testclient import TestClient
from main import app


def test_root_health() -> None:
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
