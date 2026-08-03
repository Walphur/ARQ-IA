"""Targeted checks for E01-F01 REQUEST_CHANGES resolution."""

import ast
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from infrastructure.observability.setup import configure_observability, reset_observability_for_tests


def test_access_log_feature_is_http_not_observability():
    source = Path(__file__).resolve().parents[1] / "infrastructure/observability/service.py"
    text = source.read_text(encoding="utf-8")
    assert 'feature="http"' in text
    assert 'feature="observability"' not in text


def test_setup_does_not_import_null_logger():
    path = Path(__file__).resolve().parents[1] / "infrastructure/observability/setup.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (node.module or "").endswith("adapters.null"):
            names = {alias.name for alias in node.names}
            assert "NullLogger" not in names


def test_http_middleware_is_not_base_http_middleware():
    path = Path(__file__).resolve().parents[1] / "infrastructure/observability/http.py"
    text = path.read_text(encoding="utf-8")
    assert "BaseHTTPMiddleware" not in text


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("OBS_MODE", "basic")
    monkeypatch.setenv("APP_ENV", "dev")
    monkeypatch.delenv("METRICS_TOKEN", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    reset_observability_for_tests()
    configure_observability()
    import main

    return TestClient(main.app)


def test_health_still_works_after_asgi_middleware(client):
    res = client.get("/health", headers={"X-Request-Id": "asgi-ok"})
    assert res.status_code == 200
    assert res.headers.get("X-Request-Id") == "asgi-ok"
