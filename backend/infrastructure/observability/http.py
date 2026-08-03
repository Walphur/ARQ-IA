"""HTTP middleware and /metrics endpoint wired to ObservabilityService."""

from __future__ import annotations

from typing import Callable

from fastapi import APIRouter, Header, HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from infrastructure.observability.setup import get_observability
from infrastructure.observability.taxonomy import normalize_route_template


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        obs = get_observability()
        incoming = request.headers.get("x-request-id")
        request_id = obs.ids.sanitize_request_id(incoming)
        token = obs.bind(
            request_id=request_id,
            environment=obs.settings.environment,
            version=obs.settings.app_version,
            component="api",
            module="http",
            feature="observability",
            organization_id=None,
            workspace_id=None,
            user_id=None,
            tenant_id=None,
            project_id=None,
            job_id=None,
        )
        started = obs.clock.monotonic()
        route_template = normalize_route_template(request.url.path)
        status_code = 500
        try:
            with obs.start_span(
                "http.request",
                {
                    "http.method": request.method,
                    "http.route": route_template,
                    "request_id": request_id,
                },
            ):
                # Bind backend-only trace id into context for logs.
                trace_id = obs.get_trace_id()
                if trace_id:
                    obs.bind(trace_id=trace_id)
                response = await call_next(request)
                status_code = response.status_code
                response.headers["X-Request-Id"] = request_id
                return response
        except Exception:
            obs.error("http_unhandled_error", feature="observability", module="http", route_template=route_template)
            raise
        finally:
            duration = obs.clock.monotonic() - started
            if route_template != "/metrics":
                obs.record_http(
                    route_template=route_template,
                    status_code=status_code,
                    duration_seconds=duration,
                )
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
        # If a token is configured in non-prod, enforce it when present.
        raise HTTPException(status_code=401, detail="metrics unauthorized")

    body = obs.render_metrics()
    return Response(content=body, media_type="text/plain; version=0.0.4; charset=utf-8")
