"""Context taxonomy and metrics label allowlist for E01-F01."""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Optional

# Mandatory / optional context fields (nullable when not applicable).
CONTEXT_FIELDS = (
    "request_id",
    "trace_id",
    "tenant_id",
    "project_id",
    "job_id",
    "user_id",
    "workspace_id",
    "organization_id",
    "feature",
    "module",
    "component",
    "version",
    "environment",
)

METRIC_LABEL_ALLOWLIST = frozenset(
    {
        "service",
        "env",
        "environment",
        "route_template",
        "status_class",
        "plan",
        "component",
        "module",
        "feature",
        "version",
    }
)

FORBIDDEN_METRIC_LABELS = frozenset(
    {
        "email",
        "password",
        "token",
        "authorization",
        "filename",
        "project_name",
        "query",
        "user_email",
    }
)

STATUS_CLASSES = frozenset({"2xx", "3xx", "4xx", "5xx"})


def status_class_from_code(status_code: int) -> str:
    if status_code < 300:
        return "2xx"
    if status_code < 400:
        return "3xx"
    if status_code < 500:
        return "4xx"
    return "5xx"


def normalize_route_template(path: str) -> str:
    """Collapse numeric path segments to {id} to control cardinality."""
    if not path:
        return "/"
    parts = []
    for seg in path.split("/"):
        if not seg:
            continue
        if seg.isdigit():
            parts.append("{id}")
        else:
            parts.append(seg)
    return "/" + "/".join(parts) if parts else "/"


def filter_metric_labels(labels: Mapping[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in labels.items():
        if key in FORBIDDEN_METRIC_LABELS:
            continue
        if key not in METRIC_LABEL_ALLOWLIST:
            continue
        if value is None:
            continue
        text = str(value)
        if len(text) > 64:
            text = text[:64]
        out[key] = text
    return out


def pick_context_fields(fields: Mapping[str, Any], extra: Optional[Iterable[str]] = None) -> dict[str, Any]:
    allowed = set(CONTEXT_FIELDS)
    if extra:
        allowed.update(extra)
    return {k: v for k, v in fields.items() if k in allowed and v is not None}
