from infrastructure.observability.redaction import redact_mapping, redact_message
from infrastructure.observability.taxonomy import CONTEXT_FIELDS, filter_metric_labels


def test_redacts_password_and_token():
    data = redact_mapping({"password": "secret", "token": "abc", "ok": 1})
    assert data["password"] == "[REDACTED]"
    assert data["token"] == "[REDACTED]"
    assert data["ok"] == 1


def test_redacts_suspicious_message():
    assert redact_message("user password=123") == "[REDACTED_MESSAGE]"


def test_taxonomy_includes_extended_fields():
    for field in (
        "user_id",
        "workspace_id",
        "organization_id",
        "feature",
        "module",
        "component",
        "version",
        "environment",
    ):
        assert field in CONTEXT_FIELDS


def test_metric_label_allowlist_drops_email():
    labels = filter_metric_labels({"email": "a@b.c", "route_template": "/health", "status_class": "2xx"})
    assert "email" not in labels
    assert labels["route_template"] == "/health"
