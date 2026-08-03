"""Ports for observability. Domain and app code must depend only on these protocols."""

from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Any, Mapping, Optional, Protocol, runtime_checkable


@runtime_checkable
class ClockPort(Protocol):
    def now_unix(self) -> float:
        """UTC unix timestamp in seconds."""

    def monotonic(self) -> float:
        """Monotonic seconds for durations."""


@runtime_checkable
class IdGeneratorPort(Protocol):
    def new_request_id(self) -> str:
        """Generate a new opaque request/correlation id."""

    def sanitize_request_id(self, raw: Optional[str]) -> str:
        """Validate/truncate inbound request id or generate a new one."""


@runtime_checkable
class LoggerPort(Protocol):
    def emit(self, level: str, message: str, fields: Mapping[str, Any]) -> None:
        """Emit one structured log line. Implementations must redact secrets."""


@runtime_checkable
class SpanPort(Protocol):
    def set_attribute(self, key: str, value: Any) -> None: ...

    def record_exception(self, exc: BaseException) -> None: ...

    def end(self) -> None: ...


@runtime_checkable
class TracerPort(Protocol):
    def start_span(self, name: str, attributes: Mapping[str, Any]) -> AbstractContextManager[SpanPort]:
        """Start a span; may be a no-op context manager."""

    def get_trace_id(self) -> Optional[str]:
        """Backend-only trace id (never a frontend contract)."""


@runtime_checkable
class MetricsPort(Protocol):
    def inc_request(self, *, route_template: str, status_class: str) -> None: ...

    def observe_latency(self, seconds: float, *, route_template: str, status_class: str) -> None: ...

    def set_component_status(self, component: str, status: str) -> None:
        """Extensible component health gauge (ok|fail|skipped|timeout|unknown)."""

    def set_ready(self, value: bool) -> None:
        """Aggregate readiness gauge (platform_ready)."""

    def set_platform_mode(self, mode: str) -> None:
        """Platform mode gauge (normal|degraded|maintenance|readonly)."""

    def render_exposition(self) -> str:
        """Vendor-neutral exposition text (Prometheus format allowed only inside adapter)."""
