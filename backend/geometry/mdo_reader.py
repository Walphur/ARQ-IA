"""Read-only access to mdo_* tables for Geometry.

Uses SQLAlchemy Core against known table/column names.
Does not import mdo.service, mdo.http, or perception modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from sqlalchemy import MetaData, Table, select
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.orm import Session


@dataclass(frozen=True)
class MdoElementSnapshot:
    id: str
    studio_id: int
    project_id: int
    version_id: str
    element_type: str
    discipline_code: str
    params: dict[str, Any]
    space_area_m2: Optional[float]


class MdoReader:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._meta = MetaData()
        self._versions = Table("mdo_project_versions", self._meta, autoload_with=engine)
        self._elements = Table("mdo_elements", self._meta, autoload_with=engine)
        self._param_sets = Table("mdo_parameter_sets", self._meta, autoload_with=engine)
        self._spaces = Table("mdo_spaces", self._meta, autoload_with=engine)

    def get_version_scope(
        self, conn: Connection, *, version_id: str, studio_id: int
    ) -> Optional[tuple[int, int]]:
        row = (
            conn.execute(
                select(
                    self._versions.c.studio_id,
                    self._versions.c.project_id,
                    self._versions.c.deleted_at,
                ).where(self._versions.c.id == version_id)
            )
            .mappings()
            .first()
        )
        if row is None or row["deleted_at"] is not None:
            return None
        if int(row["studio_id"]) != studio_id:
            return None
        return int(row["studio_id"]), int(row["project_id"])

    def list_element_snapshots(
        self, conn: Connection, *, version_id: str
    ) -> list[MdoElementSnapshot]:
        el = self._elements
        ps = self._param_sets
        sp = self._spaces

        rows = (
            conn.execute(
                select(
                    el.c.id,
                    el.c.studio_id,
                    el.c.project_id,
                    el.c.version_id,
                    el.c.element_type,
                    el.c.discipline_code,
                    el.c.space_id,
                    ps.c.data,
                    sp.c.area_m2.label("space_area_m2"),
                )
                .select_from(
                    el.outerjoin(
                        ps,
                        (ps.c.owner_id == el.c.id)
                        & (ps.c.owner_kind == "element")
                        & (ps.c.version_id == el.c.version_id)
                        & (ps.c.deleted_at.is_(None)),
                    ).outerjoin(
                        sp,
                        (sp.c.id == el.c.space_id) & (sp.c.deleted_at.is_(None)),
                    )
                )
                .where(el.c.version_id == version_id)
                .where(el.c.deleted_at.is_(None))
                .order_by(el.c.created_at.asc())
            )
            .mappings()
            .all()
        )

        out: list[MdoElementSnapshot] = []
        for row in rows:
            data = row["data"] if isinstance(row["data"], dict) else {}
            params = data.get("params") if isinstance(data.get("params"), dict) else {}
            space_area = row["space_area_m2"]
            out.append(
                MdoElementSnapshot(
                    id=str(row["id"]),
                    studio_id=int(row["studio_id"]),
                    project_id=int(row["project_id"]),
                    version_id=str(row["version_id"]),
                    element_type=str(row["element_type"]),
                    discipline_code=str(row["discipline_code"]),
                    params=params,
                    space_area_m2=float(space_area) if space_area is not None else None,
                )
            )
        return out


def reader_from_session(db: Session) -> MdoReader:
    return MdoReader(db.get_bind())
