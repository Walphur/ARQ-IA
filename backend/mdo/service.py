"""Casos de uso MDO — Fases 2–3: versions + jerarquía espacial."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Optional

from sqlalchemy.orm import Session

from mdo.enums import MUTABLE_VERSION_STATUSES, DomainEventType, VersionStatus
from mdo.models import Building, DomainEvent, Level, ProjectVersion, Site, Space
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

    def get_tree(self, version_id: str) -> dict[str, Any]:
        version = self._get_version(version_id)
        return {
            "version": version,
            "sites": self._alive(Site, version.id),
            "buildings": self._alive(Building, version.id),
            "levels": self._alive(Level, version.id),
            "spaces": self._alive(Space, version.id),
        }

    def _alive(self, model, version_id: str):
        return (
            self.db.query(model)
            .filter(model.version_id == version_id, model.deleted_at.is_(None))
            .all()
        )

    def _touch(self, entity) -> None:
        entity.updated_by = self.user_id
        entity.updated_at = self._now()

    def _soft_delete(self, entity) -> None:
        entity.deleted_at = self._now()
        self._touch(entity)

    def _get_owned(self, model, entity_id: str):
        entity = self.db.get(model, entity_id)
        if (
            not entity
            or getattr(entity, "deleted_at", None) is not None
            or entity.studio_id != self.studio_id
        ):
            raise MdoNotFoundError(f"{model.__name__} no encontrado.")
        return entity

    def _apply_updates(self, entity, data, fields: tuple[str, ...]) -> None:
        payload = data.model_dump(exclude_unset=True)
        for field in fields:
            if field in payload:
                setattr(entity, field, payload[field])
        self._touch(entity)

    # --- Site ---
    def create_site(self, version_id: str, data) -> Site:
        version = self._get_version(version_id)
        self._require_mutable(version)
        site = Site(
            version_id=version.id,
            studio_id=version.studio_id,
            project_id=version.project_id,
            code=data.code,
            display_name=data.display_name,
            external_id=data.external_id,
            lot_ref=data.lot_ref,
            area_m2=data.area_m2,
            created_by=self.user_id,
            updated_by=self.user_id,
        )
        self.db.add(site)
        self.db.flush()
        self._emit(
            DomainEventType.SITE_CREATED,
            project_id=version.project_id,
            version_id=version.id,
            payload={"site_id": site.id},
        )
        self.db.commit()
        self.db.refresh(site)
        return site

    def update_site(self, site_id: str, data) -> Site:
        site = self._get_owned(Site, site_id)
        self._require_mutable(self._get_version(site.version_id))
        self._apply_updates(
            site, data, ("code", "display_name", "external_id", "lot_ref", "area_m2")
        )
        self._emit(
            DomainEventType.SITE_UPDATED,
            project_id=site.project_id,
            version_id=site.version_id,
            payload={"site_id": site.id},
        )
        self.db.commit()
        self.db.refresh(site)
        return site

    def delete_site(self, site_id: str) -> Site:
        site = self._get_owned(Site, site_id)
        self._require_mutable(self._get_version(site.version_id))
        self._soft_delete(site)
        self._emit(
            DomainEventType.SITE_DELETED,
            project_id=site.project_id,
            version_id=site.version_id,
            payload={"site_id": site.id},
        )
        self.db.commit()
        self.db.refresh(site)
        return site

    # --- Building ---
    def create_building(self, version_id: str, data) -> Building:
        version = self._get_version(version_id)
        self._require_mutable(version)
        site = self._get_owned(Site, data.site_id)
        if site.version_id != version.id:
            raise MdoValidationError("site_id no pertenece a esta versión.")
        building = Building(
            version_id=version.id,
            studio_id=version.studio_id,
            project_id=version.project_id,
            site_id=site.id,
            code=data.code,
            display_name=data.display_name,
            external_id=data.external_id,
            typology=data.typology,
            created_by=self.user_id,
            updated_by=self.user_id,
        )
        self.db.add(building)
        self.db.flush()
        self._emit(
            DomainEventType.BUILDING_CREATED,
            project_id=version.project_id,
            version_id=version.id,
            payload={"building_id": building.id, "site_id": site.id},
        )
        self.db.commit()
        self.db.refresh(building)
        return building

    def update_building(self, building_id: str, data) -> Building:
        building = self._get_owned(Building, building_id)
        self._require_mutable(self._get_version(building.version_id))
        self._apply_updates(
            building, data, ("code", "display_name", "external_id", "typology")
        )
        self._emit(
            DomainEventType.BUILDING_UPDATED,
            project_id=building.project_id,
            version_id=building.version_id,
            payload={"building_id": building.id},
        )
        self.db.commit()
        self.db.refresh(building)
        return building

    def delete_building(self, building_id: str) -> Building:
        building = self._get_owned(Building, building_id)
        self._require_mutable(self._get_version(building.version_id))
        self._soft_delete(building)
        self._emit(
            DomainEventType.BUILDING_DELETED,
            project_id=building.project_id,
            version_id=building.version_id,
            payload={"building_id": building.id},
        )
        self.db.commit()
        self.db.refresh(building)
        return building

    # --- Level ---
    def create_level(self, version_id: str, data) -> Level:
        version = self._get_version(version_id)
        self._require_mutable(version)
        building = self._get_owned(Building, data.building_id)
        if building.version_id != version.id:
            raise MdoValidationError("building_id no pertenece a esta versión.")
        level = Level(
            version_id=version.id,
            studio_id=version.studio_id,
            project_id=version.project_id,
            building_id=building.id,
            code=data.code,
            display_name=data.display_name,
            external_id=data.external_id,
            elevation_m=data.elevation_m,
            sort_order=data.sort_order,
            created_by=self.user_id,
            updated_by=self.user_id,
        )
        self.db.add(level)
        self.db.flush()
        self._emit(
            DomainEventType.LEVEL_CREATED,
            project_id=version.project_id,
            version_id=version.id,
            payload={"level_id": level.id, "building_id": building.id},
        )
        self.db.commit()
        self.db.refresh(level)
        return level

    def update_level(self, level_id: str, data) -> Level:
        level = self._get_owned(Level, level_id)
        self._require_mutable(self._get_version(level.version_id))
        self._apply_updates(
            level,
            data,
            ("code", "display_name", "external_id", "elevation_m", "sort_order"),
        )
        self._emit(
            DomainEventType.LEVEL_UPDATED,
            project_id=level.project_id,
            version_id=level.version_id,
            payload={"level_id": level.id},
        )
        self.db.commit()
        self.db.refresh(level)
        return level

    def delete_level(self, level_id: str) -> Level:
        level = self._get_owned(Level, level_id)
        self._require_mutable(self._get_version(level.version_id))
        self._soft_delete(level)
        self._emit(
            DomainEventType.LEVEL_DELETED,
            project_id=level.project_id,
            version_id=level.version_id,
            payload={"level_id": level.id},
        )
        self.db.commit()
        self.db.refresh(level)
        return level

    # --- Space ---
    def create_space(self, version_id: str, data) -> Space:
        version = self._get_version(version_id)
        self._require_mutable(version)
        level = self._get_owned(Level, data.level_id)
        if level.version_id != version.id:
            raise MdoValidationError("level_id no pertenece a esta versión.")
        space = Space(
            version_id=version.id,
            studio_id=version.studio_id,
            project_id=version.project_id,
            level_id=level.id,
            code=data.code,
            display_name=data.display_name,
            external_id=data.external_id,
            space_type=data.space_type,
            area_m2=data.area_m2,
            created_by=self.user_id,
            updated_by=self.user_id,
        )
        self.db.add(space)
        self.db.flush()
        self._emit(
            DomainEventType.SPACE_CREATED,
            project_id=version.project_id,
            version_id=version.id,
            payload={"space_id": space.id, "level_id": level.id},
        )
        self.db.commit()
        self.db.refresh(space)
        return space

    def update_space(self, space_id: str, data) -> Space:
        space = self._get_owned(Space, space_id)
        self._require_mutable(self._get_version(space.version_id))
        self._apply_updates(
            space,
            data,
            ("code", "display_name", "external_id", "space_type", "area_m2"),
        )
        self._emit(
            DomainEventType.SPACE_UPDATED,
            project_id=space.project_id,
            version_id=space.version_id,
            payload={"space_id": space.id},
        )
        self.db.commit()
        self.db.refresh(space)
        return space

    def delete_space(self, space_id: str) -> Space:
        space = self._get_owned(Space, space_id)
        self._require_mutable(self._get_version(space.version_id))
        self._soft_delete(space)
        self._emit(
            DomainEventType.SPACE_DELETED,
            project_id=space.project_id,
            version_id=space.version_id,
            payload={"space_id": space.id},
        )
        self.db.commit()
        self.db.refresh(space)
        return space


__all__ = [
    "MdoService",
    "MdoNotFoundError",
    "MdoForbiddenError",
    "MdoConflictError",
    "MdoValidationError",
]
