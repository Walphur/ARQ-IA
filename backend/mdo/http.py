"""API HTTP `/v1/mdo/*` — crece por fases. Fases 2–3: versions + espacial."""

from __future__ import annotations

from typing import Annotated, Callable, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from mdo import schemas
from mdo.service import (
    MdoConflictError,
    MdoForbiddenError,
    MdoNotFoundError,
    MdoService,
)
from mdo.typing_rules import MdoValidationError

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
        raise RuntimeError("MDO HTTP deps not bound")
    yield from _get_db()


def _user(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(_db),
):
    if _current_user is None:
        raise RuntimeError("MDO HTTP deps not bound")
    return _current_user(authorization=authorization, db=db)


def _svc(user, db: Session) -> MdoService:
    assert _project_belongs is not None
    return MdoService(
        db,
        studio_id=user.studio_id,
        user_id=user.id,
        project_belongs_to_studio=_project_belongs,
    )


def _map_error(exc: Exception) -> HTTPException:
    if isinstance(exc, MdoNotFoundError):
        return HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, MdoForbiddenError):
        return HTTPException(status_code=403, detail=str(exc))
    if isinstance(exc, MdoConflictError):
        return HTTPException(status_code=409, detail=str(exc))
    if isinstance(exc, MdoValidationError):
        return HTTPException(status_code=400, detail=str(exc))
    raise exc


router = APIRouter(prefix="/v1/mdo", tags=["mdo"])


@router.post("/projects/{project_id}/ensure")
def ensure_project(project_id: int, user=Depends(_user), db: Session = Depends(_db)):
    if _require_can_edit is None:
        raise RuntimeError("MDO HTTP deps not bound")
    _require_can_edit(user)
    try:
        version, created = _svc(user, db).ensure_project_version(project_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return {"created": created, "version": schemas.serialize_version(version)}


@router.get("/projects/{project_id}/versions")
def list_versions(project_id: int, user=Depends(_user), db: Session = Depends(_db)):
    try:
        versions = _svc(user, db).list_versions(project_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return {"items": [schemas.serialize_version(v) for v in versions]}


@router.get("/versions/{version_id}")
def get_version(version_id: str, user=Depends(_user), db: Session = Depends(_db)):
    try:
        version = _svc(user, db).get_version(version_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_version(version)


@router.post("/versions/{version_id}/seal")
def seal_version(
    version_id: str,
    body: schemas.SealVersionIn,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        version = _svc(user, db).seal_version(version_id, summary=body.summary)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_version(version)


@router.get("/projects/{project_id}/events")
def list_events(
    project_id: int,
    limit: int = Query(default=100, ge=1, le=500),
    user=Depends(_user),
    db: Session = Depends(_db),
):
    try:
        events = _svc(user, db).list_events(project_id, limit=limit)
    except Exception as exc:
        raise _map_error(exc) from exc
    return {"items": [schemas.serialize_event(e) for e in events]}


@router.get("/versions/{version_id}/tree")
def get_tree(version_id: str, user=Depends(_user), db: Session = Depends(_db)):
    try:
        tree = _svc(user, db).get_tree(version_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return {
        "version": schemas.serialize_version(tree["version"]),
        "sites": [schemas.serialize_site(x) for x in tree["sites"]],
        "buildings": [schemas.serialize_building(x) for x in tree["buildings"]],
        "levels": [schemas.serialize_level(x) for x in tree["levels"]],
        "spaces": [schemas.serialize_space(x) for x in tree["spaces"]],
        "disciplines": [schemas.serialize_discipline(x) for x in tree["disciplines"]],
        "elements": [schemas.serialize_element(x) for x in tree["elements"]],
    }


@router.post("/versions/{version_id}/sites")
def create_site(
    version_id: str,
    body: schemas.SiteCreate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        site = _svc(user, db).create_site(version_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_site(site)


@router.patch("/sites/{site_id}")
def update_site(
    site_id: str,
    body: schemas.SiteUpdate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        site = _svc(user, db).update_site(site_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_site(site)


@router.delete("/sites/{site_id}")
def delete_site(site_id: str, user=Depends(_user), db: Session = Depends(_db)):
    _require_can_edit(user)
    try:
        site = _svc(user, db).delete_site(site_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_site(site)


@router.post("/versions/{version_id}/buildings")
def create_building(
    version_id: str,
    body: schemas.BuildingCreate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        building = _svc(user, db).create_building(version_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_building(building)


@router.patch("/buildings/{building_id}")
def update_building(
    building_id: str,
    body: schemas.BuildingUpdate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        building = _svc(user, db).update_building(building_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_building(building)


@router.delete("/buildings/{building_id}")
def delete_building(building_id: str, user=Depends(_user), db: Session = Depends(_db)):
    _require_can_edit(user)
    try:
        building = _svc(user, db).delete_building(building_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_building(building)


@router.post("/versions/{version_id}/levels")
def create_level(
    version_id: str,
    body: schemas.LevelCreate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        level = _svc(user, db).create_level(version_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_level(level)


@router.patch("/levels/{level_id}")
def update_level(
    level_id: str,
    body: schemas.LevelUpdate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        level = _svc(user, db).update_level(level_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_level(level)


@router.delete("/levels/{level_id}")
def delete_level(level_id: str, user=Depends(_user), db: Session = Depends(_db)):
    _require_can_edit(user)
    try:
        level = _svc(user, db).delete_level(level_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_level(level)


@router.post("/versions/{version_id}/spaces")
def create_space(
    version_id: str,
    body: schemas.SpaceCreate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        space = _svc(user, db).create_space(version_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_space(space)


@router.patch("/spaces/{space_id}")
def update_space(
    space_id: str,
    body: schemas.SpaceUpdate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        space = _svc(user, db).update_space(space_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_space(space)


@router.delete("/spaces/{space_id}")
def delete_space(space_id: str, user=Depends(_user), db: Session = Depends(_db)):
    _require_can_edit(user)
    try:
        space = _svc(user, db).delete_space(space_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_space(space)


@router.post("/versions/{version_id}/disciplines")
def create_discipline(
    version_id: str,
    body: schemas.DisciplineCreate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        disc = _svc(user, db).create_discipline(version_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_discipline(disc)


@router.patch("/disciplines/{discipline_id}")
def update_discipline(
    discipline_id: str,
    body: schemas.DisciplineUpdate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        disc = _svc(user, db).update_discipline(discipline_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_discipline(disc)


@router.delete("/disciplines/{discipline_id}")
def delete_discipline(discipline_id: str, user=Depends(_user), db: Session = Depends(_db)):
    _require_can_edit(user)
    try:
        disc = _svc(user, db).delete_discipline(discipline_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_discipline(disc)


@router.post("/versions/{version_id}/elements")
def create_element(
    version_id: str,
    body: schemas.ElementCreate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        el = _svc(user, db).create_element(version_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_element(el)


@router.patch("/elements/{element_id}")
def update_element(
    element_id: str,
    body: schemas.ElementUpdate,
    user=Depends(_user),
    db: Session = Depends(_db),
):
    _require_can_edit(user)
    try:
        el = _svc(user, db).update_element(element_id, body)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_element(el)


@router.delete("/elements/{element_id}")
def delete_element(element_id: str, user=Depends(_user), db: Session = Depends(_db)):
    _require_can_edit(user)
    try:
        el = _svc(user, db).delete_element(element_id)
    except Exception as exc:
        raise _map_error(exc) from exc
    return schemas.serialize_element(el)
