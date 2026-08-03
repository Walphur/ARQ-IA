from __future__ import annotations

from typing import Any, Optional

from sqlalchemy.orm import Session

from geometry.models import GeometryDomainEvent


def emit_event(
    db: Session,
    *,
    studio_id: int,
    project_id: int,
    version_id: Optional[str],
    event_type: str,
    payload: dict[str, Any],
    created_by: Optional[int] = None,
) -> GeometryDomainEvent:
    event = GeometryDomainEvent(
        studio_id=studio_id,
        project_id=project_id,
        version_id=version_id,
        event_type=event_type,
        payload=payload,
        created_by=created_by,
    )
    db.add(event)
    return event
