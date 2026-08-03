"""PII / secret redaction for structured logs."""

from __future__ import annotations

from typing import Any, Mapping

REDACT_KEYS = frozenset(
    {
        "password",
        "passwd",
        "secret",
        "token",
        "access_token",
        "refresh_token",
        "authorization",
        "api_key",
        "apikey",
        "mp_access_token",
        "resend_api_key",
        "credit_card",
        "card_number",
    }
)

REDACTED = "[REDACTED]"


def redact_value(key: str, value: Any) -> Any:
    lower = key.lower()
    if lower in REDACT_KEYS or lower.endswith("_token") or lower.endswith("_secret"):
        return REDACTED
    if lower in {"authorization"} and isinstance(value, str):
        return REDACTED
    if isinstance(value, Mapping):
        return redact_mapping(value)
    if isinstance(value, list):
        return [redact_value(key, item) if not isinstance(item, Mapping) else redact_mapping(item) for item in value]
    return value


def redact_mapping(data: Mapping[str, Any]) -> dict[str, Any]:
    return {str(k): redact_value(str(k), v) for k, v in data.items()}


def redact_message(message: str) -> str:
    # Keep simple: avoid dumping secrets from free-form messages in F01.
    lowered = message.lower()
    if "password" in lowered or "bearer " in lowered or "secret_key" in lowered:
        return "[REDACTED_MESSAGE]"
    return message
