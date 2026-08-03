"""HTTP routes for runtime liveness/readiness/status (E01-F02)."""

from __future__ import annotations

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from infrastructure.observability.setup import get_observability
from infrastructure.runtime.setup import get_runtime

runtime_router = APIRouter(tags=["runtime"])


@runtime_router.get("/ready")
@runtime_router.get("/api/ready")
def ready_endpoint():
    report = get_runtime().readiness()
    return JSONResponse(status_code=report.http_status, content=report.to_public_dict())


@runtime_router.get("/v1/platform/status")
def platform_status_endpoint(request: Request):
    """
    Publishes operational platform state for Studio (DegradationBanner).

    Does not own dependency checks: projects RuntimeStatusService state
    (PLATFORM_MODE + last/projected readiness). No request enforcement.
    """
    obs = get_observability()
    request_id = obs.get_request_id() or request.headers.get("x-request-id")
    status = get_runtime().platform_status(request_id=request_id)
    return status.to_public_dict()


@runtime_router.get("/v1/platform/version")
def platform_version_endpoint(request: Request):
    obs = get_observability()
    request_id = obs.get_request_id() or request.headers.get("x-request-id")
    return get_runtime().platform_version(request_id=request_id)
