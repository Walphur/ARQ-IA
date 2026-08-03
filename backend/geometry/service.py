"""Casos de uso Geometry — compute por ProjectVersion + listados."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Callable, Optional

from sqlalchemy.orm import Session

from geometry.compute import compute_element_geometry
from geometry.enums import (
    EVENT_COMPUTE_COMPLETED,
    EVENT_COMPUTE_FAILED,
    EVENT_COMPUTE_STARTED,
)
from geometry.events import emit_event
from geometry.mdo_reader import MdoReader, reader_from_session
from geometry.models import ElementGeometry, GeometryIssue
from geometry.validators import IssueDraft


class GeometryNotFoundError(LookupError):
    pass


class GeometryForbiddenError(PermissionError):
    pass


class GeometryService:
    def __init__(
        self,
        db: Session,
        *,
        studio_id: int,
        user_id: int,
        project_belongs_to_studio: Callable[[Session, int, int], bool],
        mdo_reader: Optional[MdoReader] = None,
    ):
        self.db = db
        self.studio_id = studio_id
        self.user_id = user_id
        self._project_belongs = project_belongs_to_studio
        self._reader = mdo_reader or reader_from_session(db)

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _assert_project(self, project_id: int) -> None:
        if not self._project_belongs(self.db, project_id, self.studio_id):
            raise GeometryNotFoundError("Proyecto no encontrado.")

    def _version_scope(self, version_id: str) -> tuple[int, int]:
        conn = self.db.connection()
        scope = self._reader.get_version_scope(
            conn, version_id=version_id, studio_id=self.studio_id
        )
        if scope is None:
            raise GeometryNotFoundError("Versión MDO no encontrada.")
        studio_id, project_id = scope
        self._assert_project(project_id)
        return studio_id, project_id

    def compute_for_version(self, version_id: str) -> dict:
        studio_id, project_id = self._version_scope(version_id)
        compute_run_id = str(uuid.uuid4())
        now = self._now()

        emit_event(
            self.db,
            studio_id=studio_id,
            project_id=project_id,
            version_id=version_id,
            event_type=EVENT_COMPUTE_STARTED,
            payload={"compute_run_id": compute_run_id},
            created_by=self.user_id,
        )

        try:
            conn = self.db.connection()
            snapshots = self._reader.list_element_snapshots(conn, version_id=version_id)

            # Soft-delete previous active geometries/issues for this version.
            (
                self.db.query(ElementGeometry)
                .filter(
                    ElementGeometry.version_id == version_id,
                    ElementGeometry.studio_id == studio_id,
                    ElementGeometry.deleted_at.is_(None),
                )
                .update({"deleted_at": now, "updated_at": now, "updated_by": self.user_id})
            )
            (
                self.db.query(GeometryIssue)
                .filter(
                    GeometryIssue.version_id == version_id,
                    GeometryIssue.studio_id == studio_id,
                    GeometryIssue.deleted_at.is_(None),
                )
                .update({"deleted_at": now})
            )

            geometries: list[ElementGeometry] = []
            issues: list[GeometryIssue] = []

            for snap in snapshots:
                computed = compute_element_geometry(
                    element_id=snap.id,
                    element_type=snap.element_type,
                    discipline_code=snap.discipline_code,
                    params=snap.params,
                    space_area_m2=snap.space_area_m2,
                )
                gdata = computed["geometry"]
                draft_issues: list[IssueDraft] = computed["issues"]

                geom = ElementGeometry(
                    studio_id=studio_id,
                    project_id=project_id,
                    version_id=version_id,
                    element_id=snap.id,
                    geom_type=gdata["geom_type"],
                    units=gdata.get("units") or "m",
                    length_m=gdata.get("length_m"),
                    height_m=gdata.get("height_m"),
                    thickness_m=gdata.get("thickness_m"),
                    area_m2=gdata.get("area_m2"),
                    volume_m3=gdata.get("volume_m3"),
                    bbox=gdata.get("bbox"),
                    polygon=gdata.get("polygon"),
                    centroid=gdata.get("centroid"),
                    orientation_deg=gdata.get("orientation_deg"),
                    measure_meta=gdata.get("measure_meta") or {},
                    quality_flags=gdata.get("quality_flags") or [],
                    computed_at=now,
                    compute_run_id=compute_run_id,
                    created_by=self.user_id,
                    updated_by=self.user_id,
                )
                self.db.add(geom)
                self.db.flush()
                geometries.append(geom)

                for draft in draft_issues:
                    issue = GeometryIssue(
                        studio_id=studio_id,
                        project_id=project_id,
                        version_id=version_id,
                        element_id=snap.id,
                        element_geometry_id=geom.id,
                        code=draft.code,
                        message=draft.message,
                        severity=draft.severity,
                        source=draft.source,
                        details=draft.details or {},
                        compute_run_id=compute_run_id,
                    )
                    self.db.add(issue)
                    issues.append(issue)

            emit_event(
                self.db,
                studio_id=studio_id,
                project_id=project_id,
                version_id=version_id,
                event_type=EVENT_COMPUTE_COMPLETED,
                payload={
                    "compute_run_id": compute_run_id,
                    "geometries_upserted": len(geometries),
                    "issues_created": len(issues),
                },
                created_by=self.user_id,
            )
            self.db.commit()
            for g in geometries:
                self.db.refresh(g)
            for i in issues:
                self.db.refresh(i)

            return {
                "version_id": version_id,
                "compute_run_id": compute_run_id,
                "geometries_upserted": len(geometries),
                "issues_created": len(issues),
                "geometries": geometries,
                "issues": issues,
            }
        except Exception as exc:
            self.db.rollback()
            try:
                emit_event(
                    self.db,
                    studio_id=studio_id,
                    project_id=project_id,
                    version_id=version_id,
                    event_type=EVENT_COMPUTE_FAILED,
                    payload={
                        "compute_run_id": compute_run_id,
                        "error": str(exc),
                    },
                    created_by=self.user_id,
                )
                self.db.commit()
            except Exception:
                self.db.rollback()
            raise

    def list_for_version(self, version_id: str) -> dict:
        studio_id, _project_id = self._version_scope(version_id)
        geometries = (
            self.db.query(ElementGeometry)
            .filter(
                ElementGeometry.version_id == version_id,
                ElementGeometry.studio_id == studio_id,
                ElementGeometry.deleted_at.is_(None),
            )
            .order_by(ElementGeometry.created_at.asc())
            .all()
        )
        issues = (
            self.db.query(GeometryIssue)
            .filter(
                GeometryIssue.version_id == version_id,
                GeometryIssue.studio_id == studio_id,
                GeometryIssue.deleted_at.is_(None),
            )
            .order_by(GeometryIssue.created_at.asc())
            .all()
        )
        return {
            "version_id": version_id,
            "geometries": geometries,
            "issues": issues,
        }

    def get_element_geometry(self, version_id: str, element_id: str) -> ElementGeometry:
        studio_id, _project_id = self._version_scope(version_id)
        geom = (
            self.db.query(ElementGeometry)
            .filter(
                ElementGeometry.version_id == version_id,
                ElementGeometry.element_id == element_id,
                ElementGeometry.studio_id == studio_id,
                ElementGeometry.deleted_at.is_(None),
            )
            .first()
        )
        if geom is None:
            raise GeometryNotFoundError("Geometría de elemento no encontrada.")
        return geom
