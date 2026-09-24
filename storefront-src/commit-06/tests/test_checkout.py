import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    from services.checkout import app as checkout_app
    return TestClient(checkout_app.app)


def test_healthz(client):
    assert client.get("/healthz").json() == {"ok": True}


def test_declined_charge_surfaces_reason(client, httpx_mock):
    httpx_mock.add_response(
        url="http://payments:8000/charge",
        status_code=402,
        json={"authorized": False, "reason": "insufficient_funds"},
    )
    r = client.post("/checkout", json={"cart": ["sku-1"]})
    assert r.status_code == 402
    assert "insufficient_funds" in r.text
