import pytest
from fastapi.testclient import TestClient

from infrastructure.observability.setup import configure_observability, reset_observability_for_tests


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("METRICS_TOKEN", "test-metrics-token")
    monkeypatch.delenv("RENDER", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    return TestClient(main.app)


def test_metrics_requires_token_in_prod(client):
    denied = client.get("/metrics")
    assert denied.status_code == 401
    ok = client.get("/metrics", headers={"X-Metrics-Token": "test-metrics-token"})
    assert ok.status_code == 200
    assert "arqia_http_requests_total" in ok.text


def test_metrics_bearer_token(client):
    client.get("/health")
    ok = client.get("/metrics", headers={"Authorization": "Bearer test-metrics-token"})
    assert ok.status_code == 200
