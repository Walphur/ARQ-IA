"""OpenTelemetry adapter. Only this module may import opentelemetry.*."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator, Mapping, Optional

from infrastructure.observability.adapters.null import NullSpan, NullTracer
from infrastructure.observability.ports import SpanPort


class _OtelSpan:
    def __init__(self, span: Any) -> None:
        self._span = span

    def set_attribute(self, key: str, value: Any) -> None:
        try:
            self._span.set_attribute(key, value)
        except Exception:
            return None

    def record_exception(self, exc: BaseException) -> None:
        try:
            self._span.record_exception(exc)
        except Exception:
            return None

    def end(self) -> None:
        try:
            self._span.end()
        except Exception:
            return None


def build_tracer(*, mode: str, service_name: str, endpoint: str, export: bool) -> Any:
    """Return a TracerPort. Falls back to NullTracer if OTel is unavailable or fails."""
    if mode == "off":
        return NullTracer()
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    except Exception:
        return NullTracer()

    try:
        resource = Resource.create({"service.name": service_name})
        provider = TracerProvider(resource=resource)
        if export and endpoint:
            try:
                from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

                provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
            except Exception:
                # Keep in-process tracing without failing boot.
                provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        elif mode == "full" and not endpoint:
            # Documented degrade: in-process only.
            pass
        trace.set_tracer_provider(provider)
        otel_tracer = trace.get_tracer("arqia.observability")
        return OtelTracer(otel_tracer)
    except Exception:
        return NullTracer()


class OtelTracer:
    def __init__(self, tracer: Any) -> None:
        self._tracer = tracer

    def start_span(self, name: str, attributes: Mapping[str, Any]):
        @contextmanager
        def _cm() -> Iterator[SpanPort]:
            try:
                with self._tracer.start_as_current_span(name) as span:
                    for key, value in attributes.items():
                        try:
                            span.set_attribute(key, value)
                        except Exception:
                            pass
                    wrapper = _OtelSpan(span)
                    try:
                        yield wrapper
                    except Exception as exc:
                        wrapper.record_exception(exc)
                        raise
            except Exception:
                # Never break request path because of tracing.
                span = NullSpan()
                try:
                    yield span
                finally:
                    span.end()

        return _cm()

    def get_trace_id(self) -> Optional[str]:
        """Read only from the current span context — never shared instance state."""
        try:
            from opentelemetry import trace

            span = trace.get_current_span()
            ctx = span.get_span_context() if span else None
            if ctx and getattr(ctx, "trace_id", 0):
                return format(ctx.trace_id, "032x")
        except Exception:
            return None
        return None
