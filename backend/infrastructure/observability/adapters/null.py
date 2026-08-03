"""No-op adapters for OBS_MODE=off and fallbacks."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator, Mapping, Optional

from infrastructure.observability.ports import SpanPort


class NullSpan:
    def set_attribute(self, key: str, value: Any) -> None:
        return None

    def record_exception(self, exc: BaseException) -> None:
        return None

    def end(self) -> None:
        return None


class NullTracer:
    def start_span(self, name: str, attributes: Mapping[str, Any]):
        @contextmanager
        def _cm() -> Iterator[SpanPort]:
            span = NullSpan()
            try:
                yield span
            finally:
                span.end()

        return _cm()

    def get_trace_id(self) -> Optional[str]:
        return None


class NullMetrics:
    def inc_request(self, *, route_template: str, status_class: str) -> None:
        return None

    def observe_latency(self, seconds: float, *, route_template: str, status_class: str) -> None:
        return None

    def set_component_status(self, component: str, status: str) -> None:
        return None

    def set_ready(self, value: bool) -> None:
        return None

    def set_platform_mode(self, mode: str) -> None:
        return None

    def render_exposition(self) -> str:
        return "# observability metrics disabled\n"


class NullLogger:
    def emit(self, level: str, message: str, fields: Mapping[str, Any]) -> None:
        return None
