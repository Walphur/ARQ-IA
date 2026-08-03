import pytest
from fastapi.testclient import TestClient

from infrastructure.observability.config import ObservabilitySettings
from infrastructure.observability.setup import configure_observability, get_observability, reset_observability_for_tests


def _reload_app(monkeypatch, mode: str):
    monkeypatch.setenv("OBS_MODE", mode)
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    return TestClient(main.app)


def test_mode_off_metrics_404(monkeypatch):
    client = _reload_app(monkeypatch, "off")
    res = client.get("/metrics")
    assert res.status_code == 404
    assert get_observability().get_trace_id() in (None, "")


def test_mode_basic_metrics_ok(monkeypatch):
    client = _reload_app(monkeypatch, "basic")
    client.get("/health")
    res = client.get("/metrics")
    assert res.status_code == 200
    assert "arqia_http_requests_total" in res.text


def test_mode_full_without_endpoint_boots(monkeypatch):
    client = _reload_app(monkeypatch, "full")
    res = client.get("/health")
    assert res.status_code == 200
    assert get_observability().mode == "full"


def test_invalid_mode_defaults_basic(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "nope")
    settings = ObservabilitySettings.from_env()
    assert settings.mode == "basic"
