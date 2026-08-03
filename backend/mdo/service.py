"""Casos de uso MDO — Fases 2–5: versions, espacial, Discipline/Element, ParameterSet."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Optional

from sqlalchemy.orm import Session

from mdo.enums import (
    MUTABLE_VERSION_STATUSES,
    DomainEventType,
    ParameterOwnerKind,
    VersionStatus,
)
from mdo.models import (
    Building,
    Discipline,
    DomainEvent,
    Element,
    Level,
    ParameterSet,
    ProjectVersion,
    Site,
    Space,
)
from mdo.typing_rules import (
    MdoValidationError,
    normalize_discipline_code,
    normalize_parameter_set_data,
    validate_element_classification,
)


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
            "disciplines": self._alive(Discipline, version.id),
            "elements": self._alive(Element, version.id),
            "parameter_sets": self._alive(ParameterSet, version.id),
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

    # --- Discipline (reemplaza System ambiguo) ---
    def create_discipline(self, version_id: str, data) -> Discipline:
        version = self._get_version(version_id)
        self._require_mutable(version)
        code = normalize_discipline_code(data.code)
        dup = (
            self.db.query(Discipline)
            .filter(
                Discipline.version_id == version.id,
                Discipline.code == code,
                Discipline.deleted_at.is_(None),
            )
            .first()
        )
        if dup:
            raise MdoConflictError(f"Ya existe la disciplina '{code}' en esta versión.")
        disc = Discipline(
            version_id=version.id,
            studio_id=version.studio_id,
            project_id=version.project_id,
            code=code,
            display_name=data.display_name,
            external_id=data.external_id,
            description=data.description,
            created_by=self.user_id,
            updated_by=self.user_id,
        )
        self.db.add(disc)
        self.db.flush()
        self._emit(
            DomainEventType.DISCIPLINE_CREATED,
            project_id=version.project_id,
            version_id=version.id,
            payload={"discipline_id": disc.id, "code": code},
        )
        self.db.commit()
        self.db.refresh(disc)
        return disc

    def update_discipline(self, discipline_id: str, data) -> Discipline:
        disc = self._get_owned(Discipline, discipline_id)
        self._require_mutable(self._get_version(disc.version_id))
        self._apply_updates(disc, data, ("display_name", "external_id", "description"))
        self._emit(
            DomainEventType.DISCIPLINE_UPDATED,
            project_id=disc.project_id,
            version_id=disc.version_id,
            payload={"discipline_id": disc.id},
        )
        self.db.commit()
        self.db.refresh(disc)
        return disc

    def delete_discipline(self, discipline_id: str) -> Discipline:
        disc = self._get_owned(Discipline, discipline_id)
        self._require_mutable(self._get_version(disc.version_id))
        self._soft_delete(disc)
        self._emit(
            DomainEventType.DISCIPLINE_DELETED,
            project_id=disc.project_id,
            version_id=disc.version_id,
            payload={"discipline_id": disc.id},
        )
        self.db.commit()
        self.db.refresh(disc)
        return disc

    # --- Element ---
    def create_element(self, version_id: str, data) -> Element:
        version = self._get_version(version_id)
        self._require_mutable(version)
        d_code, e_type = validate_element_classification(
            data.discipline_code, data.element_type
        )
        level_id = data.level_id
        space_id = data.space_id
        discipline_id = data.discipline_id
        if level_id:
            level = self._get_owned(Level, level_id)
            if level.version_id != version.id:
                raise MdoValidationError("level_id no pertenece a esta versión.")
        if space_id:
            space = self._get_owned(Space, space_id)
            if space.version_id != version.id:
                raise MdoValidationError("space_id no pertenece a esta versión.")
            if level_id and space.level_id != level_id:
                raise MdoValidationError("space_id no pertenece al level_id indicado.")
        if discipline_id:
            disc = self._get_owned(Discipline, discipline_id)
            if disc.version_id != version.id:
                raise MdoValidationError("discipline_id no pertenece a esta versión.")
            if disc.code != d_code:
                raise MdoValidationError(
                    "discipline_code no coincide con la Discipline referenciada."
                )
        el = Element(
            version_id=version.id,
            studio_id=version.studio_id,
            project_id=version.project_id,
            level_id=level_id,
            space_id=space_id,
            discipline_id=discipline_id,
            discipline_code=d_code,
            element_type=e_type,
            code=data.code,
            display_name=data.display_name,
            external_id=data.external_id,
            created_by=self.user_id,
            updated_by=self.user_id,
        )
        self.db.add(el)
        self.db.flush()
        self._emit(
            DomainEventType.ELEMENT_CREATED,
            project_id=version.project_id,
            version_id=version.id,
            payload={
                "element_id": el.id,
                "discipline_code": d_code,
                "element_type": e_type,
            },
        )
        self.db.commit()
        self.db.refresh(el)
        return el

    def update_element(self, element_id: str, data) -> Element:
        el = self._get_owned(Element, element_id)
        self._require_mutable(self._get_version(el.version_id))
        payload = data.model_dump(exclude_unset=True)
        if "discipline_code" in payload or "element_type" in payload:
            d_code, e_type = validate_element_classification(
                payload.get("discipline_code", el.discipline_code),
                payload.get("element_type", el.element_type),
            )
            el.discipline_code = d_code
            el.element_type = e_type
        for field in (
            "display_name",
            "code",
            "external_id",
            "level_id",
            "space_id",
            "discipline_id",
        ):
            if field in payload:
                setattr(el, field, payload[field])
        if el.discipline_id:
            disc = self._get_owned(Discipline, el.discipline_id)
            if disc.code != el.discipline_code:
                raise MdoValidationError(
                    "discipline_code no coincide con la Discipline referenciada."
                )
        self._touch(el)
        self._emit(
            DomainEventType.ELEMENT_UPDATED,
            project_id=el.project_id,
            version_id=el.version_id,
            payload={"element_id": el.id},
        )
        self.db.commit()
        self.db.refresh(el)
        return el

    def delete_element(self, element_id: str) -> Element:
        el = self._get_owned(Element, element_id)
        self._require_mutable(self._get_version(el.version_id))
        self._soft_delete(el)
        self._emit(
            DomainEventType.ELEMENT_DELETED,
            project_id=el.project_id,
            version_id=el.version_id,
            payload={"element_id": el.id},
        )
        self.db.commit()
        self.db.refresh(el)
        return el

    # --- ParameterSet (solo params/metadata) ---
    def upsert_parameter_set(self, version_id: str, data) -> ParameterSet:
        version = self._get_version(version_id)
        self._require_mutable(version)
        try:
            owner_kind = ParameterOwnerKind(data.owner_kind).value
        except ValueError as exc:
            raise MdoValidationError(
                f"owner_kind inválido. Valores: {[k.value for k in ParameterOwnerKind]}"
            ) from exc
        self._assert_owner_exists(version.id, owner_kind, data.owner_id)
        normalized = normalize_parameter_set_data(data.data)
        existing = (
            self.db.query(ParameterSet)
            .filter(
                ParameterSet.version_id == version.id,
                ParameterSet.owner_kind == owner_kind,
                ParameterSet.owner_id == data.owner_id,
                ParameterSet.code == data.code,
                ParameterSet.deleted_at.is_(None),
            )
            .first()
        )
        if existing:
            existing.data = normalized
            existing.display_name = data.display_name
            existing.external_id = data.external_id
            existing.schema_version = data.schema_version
            self._touch(existing)
            ps = existing
        else:
            ps = ParameterSet(
                version_id=version.id,
                studio_id=version.studio_id,
                project_id=version.project_id,
                owner_kind=owner_kind,
                owner_id=data.owner_id,
                code=data.code,
                display_name=data.display_name,
                external_id=data.external_id,
                schema_version=data.schema_version,
                data=normalized,
                created_by=self.user_id,
                updated_by=self.user_id,
            )
            self.db.add(ps)
            self.db.flush()
        self._emit(
            DomainEventType.PARAMETER_SET_UPSERTED,
            project_id=version.project_id,
            version_id=version.id,
            payload={
                "parameter_set_id": ps.id,
                "owner_kind": owner_kind,
                "owner_id": data.owner_id,
            },
        )
        self.db.commit()
        self.db.refresh(ps)
        return ps

    def delete_parameter_set(self, parameter_set_id: str) -> ParameterSet:
        ps = self._get_owned(ParameterSet, parameter_set_id)
        self._require_mutable(self._get_version(ps.version_id))
        self._soft_delete(ps)
        self._emit(
            DomainEventType.PARAMETER_SET_DELETED,
            project_id=ps.project_id,
            version_id=ps.version_id,
            payload={"parameter_set_id": ps.id},
        )
        self.db.commit()
        self.db.refresh(ps)
        return ps

    def _assert_owner_exists(self, version_id: str, owner_kind: str, owner_id: str) -> None:
        mapping = {
            ParameterOwnerKind.SITE.value: Site,
            ParameterOwnerKind.BUILDING.value: Building,
            ParameterOwnerKind.LEVEL.value: Level,
            ParameterOwnerKind.SPACE.value: Space,
            ParameterOwnerKind.DISCIPLINE.value: Discipline,
            ParameterOwnerKind.ELEMENT.value: Element,
        }
        model = mapping[owner_kind]
        owner = self._get_owned(model, owner_id)
        if owner.version_id != version_id:
            raise MdoValidationError("owner_id no pertenece a esta versión.")


__all__ = [
    "MdoService",
    "MdoNotFoundError",
    "MdoForbiddenError",
    "MdoConflictError",
    "MdoValidationError",
]
