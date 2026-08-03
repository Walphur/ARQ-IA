"""HTTP middleware and /metrics endpoint wired to ObservabilityService."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Response

from infrastructure.observability.setup import get_observability
from infrastructure.observability.taxonomy import normalize_route_template


class ObservabilityMiddleware:
    """Pure ASGI middleware so contextvars propagate into route handlers."""

    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        obs = get_observability()
        header_map = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in scope.get("headers", [])
        }
        request_id = obs.ids.sanitize_request_id(header_map.get("x-request-id"))
        token = obs.bind(
            request_id=request_id,
            environment=obs.settings.environment,
            version=obs.settings.app_version,
            component="api",
            module="http",
            organization_id=None,
            workspace_id=None,
            user_id=None,
            tenant_id=None,
            project_id=None,
            job_id=None,
        )
        started = obs.clock.monotonic()
        route_template = normalize_route_template(scope.get("path") or "/")
        status_code = 500
        trace_token: Optional[object] = None

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message.get("status", 500))
                headers = list(message.get("headers") or [])
                headers.append((b"x-request-id", request_id.encode("latin-1")))
                message = {**message, "headers": headers}
            await send(message)

        try:
            with obs.start_span(
                "http.request",
                {
                    "http.method": scope.get("method", "GET"),
                    "http.route": route_template,
                    "request_id": request_id,
                },
            ):
                trace_id = obs.get_trace_id()
                if trace_id:
                    trace_token = obs.bind(trace_id=trace_id)
                await self.app(scope, receive, send_wrapper)
        except Exception:
            obs.error(
                "http_unhandled_error",
                feature="http",
                module="http",
                route_template=route_template,
            )
            raise
        finally:
            duration = obs.clock.monotonic() - started
            if route_template != "/metrics":
                obs.record_http(
                    route_template=route_template,
                    status_code=status_code,
                    duration_seconds=duration,
                )
            if trace_token is not None:
                obs.reset(trace_token)
            obs.reset(token)


metrics_router = APIRouter(tags=["observability"])


@metrics_router.get("/metrics")
def metrics_endpoint(
    authorization: str | None = Header(default=None),
    x_metrics_token: str | None = Header(default=None, alias="X-Metrics-Token"),
):
    obs = get_observability()
    if obs.settings.mode == "off":
        raise HTTPException(status_code=404, detail="metrics disabled")

    provided = None
    if x_metrics_token:
        provided = x_metrics_token.strip()
    elif authorization and authorization.lower().startswith("bearer "):
        provided = authorization[7:].strip()

    if obs.settings.require_metrics_token:
        if not obs.settings.metrics_token or provided != obs.settings.metrics_token:
            raise HTTPException(status_code=401, detail="metrics unauthorized")
    elif obs.settings.metrics_token and provided != obs.settings.metrics_token:
        raise HTTPException(status_code=401, detail="metrics unauthorized")

    body = obs.render_metrics()
    return Response(content=body, media_type="text/plain; version=0.0.4; charset=utf-8")
