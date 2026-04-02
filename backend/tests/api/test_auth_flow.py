from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_bootstrap_and_login_flow() -> None:
    bootstrap = client.post(
        "/api/v1/auth/bootstrap-admin",
        json={"email": "api-test-admin@example.com", "password": "secret123"},
    )
    assert bootstrap.status_code in (201, 409)

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "api-test-admin@example.com", "password": "secret123"},
    )
    assert login.status_code == 200
    data = login.json()
    assert "access_token" in data
    assert "refresh_token" in data
