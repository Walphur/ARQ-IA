"""Explicit Observability service (not a generic facade)."""

from __future__ import annotations

from typing import Any, Mapping, Optional

from infrastructure.observability import context as obs_context
from infrastructure.observability.config import ObservabilitySettings
from infrastructure.observability.ports import (
    ClockPort,
    IdGeneratorPort,
    LoggerPort,
    MetricsPort,
    TracerPort,
)
from infrastructure.observability.taxonomy import pick_context_fields


class ObservabilityService:
    """Application-facing observability API. Domain must use only this service + ports."""

    def __init__(
        self,
        *,
        settings: ObservabilitySettings,
        clock: ClockPort,
        ids: IdGeneratorPort,
        logger: LoggerPort,
        tracer: TracerPort,
        metrics: MetricsPort,
    ) -> None:
        self.settings = settings
        self.clock = clock
        self.ids = ids
        self.logger = logger
        self.tracer = tracer
        self.metrics = metrics
        self._configured = True

    @property
    def mode(self) -> str:
        return self.settings.mode

    def bind(self, **fields: Any):
        return obs_context.bind(**fields)

    def reset(self, token) -> None:
        obs_context.reset(token)

    def clear(self):
        return obs_context.clear()

    def get_request_id(self) -> Optional[str]:
        value = obs_context.get_field("request_id")
        return str(value) if value is not None else None

    def get_trace_id(self) -> Optional[str]:
        # Backend-only: never a frontend contract.
        return self.tracer.get_trace_id() or obs_context.get_field("trace_id")

    def start_span(self, name: str, attributes: Optional[Mapping[str, Any]] = None):
        attrs = dict(attributes or {})
        attrs.update(pick_context_fields(obs_context.get_context()))
        return self.tracer.start_span(name, attrs)

    def info(self, message: str, **fields: Any) -> None:
        self._emit("info", message, fields)

    def warning(self, message: str, **fields: Any) -> None:
        self._emit("warning", message, fields)

    def error(self, message: str, **fields: Any) -> None:
        self._emit("error", message, fields)

    def _emit(self, level: str, message: str, fields: Mapping[str, Any]) -> None:
        if self.settings.mode == "off" and level == "info":
            return
        payload = {
            **pick_context_fields(obs_context.get_context()),
            **pick_context_fields(fields, extra=fields.keys()),
            "version": self.settings.app_version,
            "environment": self.settings.environment,
            "component": fields.get("component") or self.settings.component,
            "module": fields.get("module") or "backend",
        }
        trace_id = self.get_trace_id()
        if trace_id:
            payload["trace_id"] = trace_id
        self.logger.emit(level, message, payload)

    def record_http(
        self,
        *,
        route_template: str,
        status_code: int,
        duration_seconds: float,
    ) -> None:
        from infrastructure.observability.taxonomy import status_class_from_code

        status_class = status_class_from_code(status_code)
        if self.settings.mode != "off":
            self.metrics.inc_request(route_template=route_template, status_class=status_class)
            self.metrics.observe_latency(
                duration_seconds, route_template=route_template, status_class=status_class
            )
        self.info(
            "http_request",
            feature="observability",
            module="http",
            route_template=route_template,
            status_code=status_code,
            status_class=status_class,
            duration_ms=round(duration_seconds * 1000, 3),
        )

    def render_metrics(self) -> str:
        if self.settings.mode == "off":
            return ""
        return self.metrics.render_exposition()

    def shutdown(self) -> None:
        return None
