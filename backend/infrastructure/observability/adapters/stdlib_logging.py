"""JSON / text logging via stdlib — no vendor APM."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Mapping

from infrastructure.observability.redaction import redact_mapping, redact_message


class StdlibLoggerAdapter:
    def __init__(self, *, level: str = "INFO", fmt: str = "json", service: str = "arq-ia-api") -> None:
        self._fmt = fmt
        self._service = service
        self._logger = logging.getLogger("arqia.observability")
        self._logger.handlers.clear()
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(message)s"))
        self._logger.addHandler(handler)
        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        self._logger.propagate = False

    def emit(self, level: str, message: str, fields: Mapping[str, Any]) -> None:
        safe_fields = redact_mapping(dict(fields))
        safe_msg = redact_message(message)
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": level.upper(),
            "msg": safe_msg,
            "service": self._service,
            **safe_fields,
        }
        if self._fmt == "json":
            line = json.dumps(payload, ensure_ascii=False, default=str)
        else:
            extras = " ".join(f"{k}={v}" for k, v in safe_fields.items())
            line = f"{payload['ts']} {payload['level']} {safe_msg} {extras}".rstrip()
        log_fn = getattr(self._logger, level.lower(), self._logger.info)
        log_fn(line)
