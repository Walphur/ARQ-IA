"""Casos de uso MDO — Fase 2: ProjectVersion ensure/seal."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Optional

from sqlalchemy.orm import Session

from mdo.enums import MUTABLE_VERSION_STATUSES, DomainEventType, VersionStatus
from mdo.models import DomainEvent, ProjectVersion
from mdo.typing_rules import MdoValidationError


class MdoNotFoundError(LookupError):
    pass


class MdoForbiddenError(PermissionError):
    pass


class MdoConflictError(RuntimeError):
    pass


class MdoService:
    def __init__(
        self,
        db: Session,
        *,
        studio_id: int,
        user_id: int,
        project_belongs_to_studio: Callable[[Session, int, int], bool],
    ):
        self.db = db
        self.studio_id = studio_id
        self.user_id = user_id
        self._project_belongs = project_belongs_to_studio

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _assert_project(self, project_id: int) -> None:
        if not self._project_belongs(self.db, project_id, self.studio_id):
            raise MdoNotFoundError("Proyecto no encontrado.")

    def _emit(
        self,
        event_type: DomainEventType,
        *,
        project_id: int,
        version_id: Optional[str],
        payload: dict[str, Any],
    ) -> DomainEvent:
        ev = DomainEvent(
            studio_id=self.studio_id,
            project_id=project_id,
            version_id=version_id,
            event_type=event_type.value,
            payload=payload,
            created_by=self.user_id,
        )
        self.db.add(ev)
        return ev

    def _get_version(self, version_id: str) -> ProjectVersion:
        v = self.db.get(ProjectVersion, version_id)
        if not v or v.deleted_at is not None or v.studio_id != self.studio_id:
            raise MdoNotFoundError("Versión MDO no encontrada.")
        return v

    def _require_mutable(self, version: ProjectVersion) -> None:
        if version.status not in MUTABLE_VERSION_STATUSES:
            raise MdoConflictError(
                f"La versión está '{version.status}' y no admite escrituras in-place."
            )

    def ensure_project_version(self, project_id: int) -> tuple[ProjectVersion, bool]:
        self._assert_project(project_id)
        existing = (
            self.db.query(ProjectVersion)
            .filter(
                ProjectVersion.project_id == project_id,
                ProjectVersion.studio_id == self.studio_id,
                ProjectVersion.deleted_at.is_(None),
            )
            .order_by(ProjectVersion.version_number.asc())
            .first()
        )
        if existing:
            return existing, False
        version = ProjectVersion(
            studio_id=self.studio_id,
            project_id=project_id,
            version_number=1,
            status=VersionStatus.ACTIVE.value,
            display_name="Versión 1",
            code="v1",
            created_by=self.user_id,
            updated_by=self.user_id,
        )
        self.db.add(version)
        self.db.flush()
        self._emit(
            DomainEventType.VERSION_ENSURED,
            project_id=project_id,
            version_id=version.id,
            payload={"version_number": 1, "status": version.status},
        )
        self.db.commit()
        self.db.refresh(version)
        return version, True

    def list_versions(self, project_id: int) -> list[ProjectVersion]:
        self._assert_project(project_id)
        return (
            self.db.query(ProjectVersion)
            .filter(
                ProjectVersion.project_id == project_id,
                ProjectVersion.studio_id == self.studio_id,
                ProjectVersion.deleted_at.is_(None),
            )
            .order_by(ProjectVersion.version_number.asc())
            .all()
        )

    def get_version(self, version_id: str) -> ProjectVersion:
        return self._get_version(version_id)

    def seal_version(self, version_id: str, summary: Optional[str] = None) -> ProjectVersion:
        version = self._get_version(version_id)
        self._require_mutable(version)
        version.status = VersionStatus.SEALED.value
        version.summary = summary
        version.updated_by = self.user_id
        version.updated_at = self._now()
        self._emit(
            DomainEventType.VERSION_SEALED,
            project_id=version.project_id,
            version_id=version.id,
            payload={"summary": summary},
        )
        self.db.commit()
        self.db.refresh(version)
        return version

    def list_events(self, project_id: int, *, limit: int = 100) -> list[DomainEvent]:
        self._assert_project(project_id)
        return (
            self.db.query(DomainEvent)
            .filter(
                DomainEvent.project_id == project_id,
                DomainEvent.studio_id == self.studio_id,
            )
            .order_by(DomainEvent.created_at.desc())
            .limit(min(limit, 500))
            .all()
        )


# Re-export for HTTP error mapping consistency across phases
__all__ = [
    "MdoService",
    "MdoNotFoundError",
    "MdoForbiddenError",
    "MdoConflictError",
    "MdoValidationError",
]
