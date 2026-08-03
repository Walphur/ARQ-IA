"""DTOs Pydantic del API MDO (crece por fases)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SealVersionIn(BaseModel):
    summary: Optional[str] = None


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
