"""API HTTP `/v1/geometry/*` — E03-F02."""

from __future__ import annotations

from typing import Annotated, Callable, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from geometry import schemas
from geometry.service import GeometryNotFoundError, GeometryService

_get_db: Optional[Callable] = None
_current_user: Optional[Callable] = None
_require_can_edit: Optional[Callable] = None
_project_belongs: Optional[Callable] = None


def bind_http_deps(
    *,
    get_db: Callable,
    current_user: Callable,
    require_can_edit: Callable,
    project_belongs_to_studio: Callable,
) -> None:
    global _get_db, _current_user, _require_can_edit, _project_belongs
    _get_db = get_db
    _current_user = current_user
    _require_can_edit = require_can_edit
    _project_belongs = project_belongs_to_studio


def _db():
    if _get_db is None:
        raise RuntimeError("Geometry HTTP deps not bound")
    yield from _get_db()


def _user(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(_db),
):
    if _current_user is None:
        raise RuntimeError("Geometry HTTP deps not bound")
    return _current_user(authorization=authorization, db=db)


def _svc(user, db: Session) -> GeometryService:
    assert _project_belongs is not None
    return GeometryService(
        db,
        studio_id=user.studio_id,
        user_id=user.id,
        project_belongs_to_studio=_project_belongs,
    )


def _map_error(exc: Exception) -> HTTPException:
    if isinstance(exc, GeometryNotFoundError):
        return HTTPException(status_code=404, detail=str(exc))
    raise exc


router = APIRouter(prefix="/v1/geometry", tags=["geometry"])


@router.post("/versions/{version_id}/compute")
def compute_version(version_id: str, user=Depends(_user), db: Session = Depends(_db)):
    if _require_can_edit is None:
        raise RuntimeError("Geometry HTTP deps not bound")
    _require_can_edit(user)
    try:
        result = _svc(user, db).compute_for_version(version_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return {
        "version_id": result["version_id"],
        "compute_run_id": result["compute_run_id"],
        "geometries_upserted": result["geometries_upserted"],
        "issues_created": result["issues_created"],
        "geometries": [schemas.serialize_geometry(g) for g in result["geometries"]],
        "issues": [schemas.serialize_issue(i) for i in result["issues"]],
    }


@router.get("/versions/{version_id}")
def list_version_geometry(version_id: str, user=Depends(_user), db: Session = Depends(_db)):
    try:
        result = _svc(user, db).list_for_version(version_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return {
        "version_id": result["version_id"],
        "geometries": [schemas.serialize_geometry(g) for g in result["geometries"]],
        "issues": [schemas.serialize_issue(i) for i in result["issues"]],
    }


@router.get("/versions/{version_id}/elements/{element_id}")
def get_element_geometry(
    version_id: str,
    element_id: str,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    try:
        geom = _svc(user, db).get_element_geometry(version_id, element_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_geometry(geom)
