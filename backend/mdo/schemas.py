"""DTOs Pydantic del API MDO (crece por fases)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SealVersionIn(BaseModel):
    summary: Optional[str] = None


class ExternalIdMixin(BaseModel):
    external_id: Optional[str] = Field(default=None, max_length=120)


class SiteCreate(ExternalIdMixin):
    code: Optional[str] = Field(default=None, max_length=80)
    display_name: str = Field(min_length=1, max_length=180)
    lot_ref: Optional[str] = None
    area_m2: Optional[float] = None


class SiteUpdate(BaseModel):
    code: Optional[str] = Field(default=None, max_length=80)
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=180)
    external_id: Optional[str] = Field(default=None, max_length=120)
    lot_ref: Optional[str] = None
    area_m2: Optional[float] = None


class BuildingCreate(ExternalIdMixin):
    site_id: str
    code: Optional[str] = Field(default=None, max_length=80)
    display_name: str = Field(min_length=1, max_length=180)
    typology: Optional[str] = None


class BuildingUpdate(BaseModel):
    code: Optional[str] = Field(default=None, max_length=80)
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=180)
    external_id: Optional[str] = Field(default=None, max_length=120)
    typology: Optional[str] = None


class LevelCreate(ExternalIdMixin):
    building_id: str
    code: Optional[str] = Field(default=None, max_length=80)
    display_name: str = Field(min_length=1, max_length=180)
    elevation_m: Optional[float] = None
    sort_order: int = 0


class LevelUpdate(BaseModel):
    code: Optional[str] = Field(default=None, max_length=80)
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=180)
    external_id: Optional[str] = Field(default=None, max_length=120)
    elevation_m: Optional[float] = None
    sort_order: Optional[int] = None


class SpaceCreate(ExternalIdMixin):
    level_id: str
    code: Optional[str] = Field(default=None, max_length=80)
    display_name: str = Field(min_length=1, max_length=180)
    space_type: Optional[str] = None
    area_m2: Optional[float] = None


class SpaceUpdate(BaseModel):
    code: Optional[str] = Field(default=None, max_length=80)
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=180)
    external_id: Optional[str] = Field(default=None, max_length=120)
    space_type: Optional[str] = None
    area_m2: Optional[float] = None


class DisciplineCreate(ExternalIdMixin):
    code: str = Field(min_length=1, max_length=64)
    display_name: str = Field(min_length=1, max_length=180)
    description: Optional[str] = None


class DisciplineUpdate(BaseModel):
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=180)
    external_id: Optional[str] = Field(default=None, max_length=120)
    description: Optional[str] = None


class ElementCreate(ExternalIdMixin):
    discipline_code: str = Field(min_length=1, max_length=64)
    element_type: str = Field(min_length=1, max_length=120)
    display_name: str = Field(min_length=1, max_length=180)
    code: Optional[str] = Field(default=None, max_length=80)
    level_id: Optional[str] = None
    space_id: Optional[str] = None
    discipline_id: Optional[str] = None


class ElementUpdate(BaseModel):
    discipline_code: Optional[str] = Field(default=None, max_length=64)
    element_type: Optional[str] = Field(default=None, max_length=120)
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=180)
    code: Optional[str] = Field(default=None, max_length=80)
    external_id: Optional[str] = Field(default=None, max_length=120)
    level_id: Optional[str] = None
    space_id: Optional[str] = None
    discipline_id: Optional[str] = None


def _dt(value: Optional[datetime]) -> Optional[str]:
    return value.isoformat() if value else None


def serialize_version(v) -> dict:
    return {
        "id": v.id,
        "studio_id": v.studio_id,
        "project_id": v.project_id,
        "version_number": v.version_number,
        "status": v.status,
        "parent_version_id": v.parent_version_id,
        "code": v.code,
        "display_name": v.display_name,
        "external_id": v.external_id,
        "summary": v.summary,
        "created_at": _dt(v.created_at),
        "updated_at": _dt(v.updated_at),
        "created_by": v.created_by,
        "updated_by": v.updated_by,
        "deleted_at": _dt(v.deleted_at),
    }


def serialize_site(s) -> dict:
    return {
        "id": s.id,
        "version_id": s.version_id,
        "studio_id": s.studio_id,
        "project_id": s.project_id,
        "code": s.code,
        "display_name": s.display_name,
        "external_id": s.external_id,
        "lot_ref": s.lot_ref,
        "area_m2": s.area_m2,
        "created_at": _dt(s.created_at),
        "updated_at": _dt(s.updated_at),
        "created_by": s.created_by,
        "updated_by": s.updated_by,
        "deleted_at": _dt(s.deleted_at),
    }


def serialize_building(b) -> dict:
    return {
        "id": b.id,
        "version_id": b.version_id,
        "site_id": b.site_id,
        "studio_id": b.studio_id,
        "project_id": b.project_id,
        "code": b.code,
        "display_name": b.display_name,
        "external_id": b.external_id,
        "typology": b.typology,
        "created_at": _dt(b.created_at),
        "updated_at": _dt(b.updated_at),
        "created_by": b.created_by,
        "updated_by": b.updated_by,
        "deleted_at": _dt(b.deleted_at),
    }


def serialize_level(lv) -> dict:
    return {
        "id": lv.id,
        "version_id": lv.version_id,
        "building_id": lv.building_id,
        "studio_id": lv.studio_id,
        "project_id": lv.project_id,
        "code": lv.code,
        "display_name": lv.display_name,
        "external_id": lv.external_id,
        "elevation_m": lv.elevation_m,
        "sort_order": lv.sort_order,
        "created_at": _dt(lv.created_at),
        "updated_at": _dt(lv.updated_at),
        "created_by": lv.created_by,
        "updated_by": lv.updated_by,
        "deleted_at": _dt(lv.deleted_at),
    }


def serialize_space(sp) -> dict:
    return {
        "id": sp.id,
        "version_id": sp.version_id,
        "level_id": sp.level_id,
        "studio_id": sp.studio_id,
        "project_id": sp.project_id,
        "code": sp.code,
        "display_name": sp.display_name,
        "external_id": sp.external_id,
        "space_type": sp.space_type,
        "area_m2": sp.area_m2,
        "created_at": _dt(sp.created_at),
        "updated_at": _dt(sp.updated_at),
        "created_by": sp.created_by,
        "updated_by": sp.updated_by,
        "deleted_at": _dt(sp.deleted_at),
    }


def serialize_discipline(d) -> dict:
    return {
        "id": d.id,
        "version_id": d.version_id,
        "studio_id": d.studio_id,
        "project_id": d.project_id,
        "code": d.code,
        "display_name": d.display_name,
        "external_id": d.external_id,
        "description": d.description,
        "created_at": _dt(d.created_at),
        "updated_at": _dt(d.updated_at),
        "created_by": d.created_by,
        "updated_by": d.updated_by,
        "deleted_at": _dt(d.deleted_at),
    }


def serialize_element(el) -> dict:
    return {
        "id": el.id,
        "version_id": el.version_id,
        "studio_id": el.studio_id,
        "project_id": el.project_id,
        "level_id": el.level_id,
        "space_id": el.space_id,
        "discipline_id": el.discipline_id,
        "discipline_code": el.discipline_code,
        "element_type": el.element_type,
        "code": el.code,
        "display_name": el.display_name,
        "external_id": el.external_id,
        "created_at": _dt(el.created_at),
        "updated_at": _dt(el.updated_at),
        "created_by": el.created_by,
        "updated_by": el.updated_by,
        "deleted_at": _dt(el.deleted_at),
    }


def serialize_event(ev) -> dict:
    return {
        "id": ev.id,
        "studio_id": ev.studio_id,
        "project_id": ev.project_id,
        "version_id": ev.version_id,
        "event_type": ev.event_type,
        "payload": ev.payload,
        "created_at": _dt(ev.created_at),
        "created_by": ev.created_by,
    }
