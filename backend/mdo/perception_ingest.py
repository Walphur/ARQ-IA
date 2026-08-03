"""Persistir propuestas Perception→MDO vía MdoService (strangler E03-F01).

No importa motor_ia. No calcula materiales/costos.
Fallas deben capturarse en el composition root (main) para no romper Process.
"""

from __future__ import annotations

from typing import Any, Optional, Type

from mdo import schemas
from mdo.models import Building, Discipline, Element, Level, Site, Space
from mdo.perception_map import map_detections_to_mdo_proposal
from mdo.service import MdoService


def _find_by_external(svc: MdoService, model: Type, version_id: str, external_id: str):
    if not external_id:
        return None
    return (
        svc.db.query(model)
        .filter(
            model.version_id == version_id,
            model.external_id == external_id,
            model.studio_id == svc.studio_id,
            model.deleted_at.is_(None),
        )
        .first()
    )


def ingest_perception_to_mdo(
    svc: MdoService,
    *,
    project_id: int,
    process_id: int,
    detections: dict[str, Any],
    project_name: str = "Obra",
) -> dict[str, Any]:
    """Ensure version + upsert Building/Level/Space/Element desde detections.

    Returns summary for Process.result_meta['mdo'].
    """
    proposal = map_detections_to_mdo_proposal(
        detections,
        process_id=process_id,
        project_name=project_name,
    )
    version, created = svc.ensure_project_version(project_id)
    vid = version.id

    ids: dict[str, Any] = {
        "ok": True,
        "version_id": vid,
        "version_created": created,
        "process_id": process_id,
        "tipo_plano": proposal.get("tipo_plano"),
        "site_id": None,
        "building_id": None,
        "level_id": None,
        "space_ids": [],
        "discipline_ids": [],
        "element_ids": [],
        "parameter_set_ids": [],
    }

    site_id = None
    if proposal.get("site"):
        site_id = _upsert_site(svc, vid, proposal["site"]).id
        ids["site_id"] = site_id

    building_id = None
    if proposal.get("building") and site_id:
        building_id = _upsert_building(svc, vid, site_id, proposal["building"]).id
        ids["building_id"] = building_id

    level_id = None
    if proposal.get("level") and building_id:
        level_id = _upsert_level(svc, vid, building_id, proposal["level"]).id
        ids["level_id"] = level_id

    space_by_ext: dict[str, str] = {}
    primary_space_id = None
    for sp in proposal.get("spaces") or []:
        if not level_id:
            break
        space = _upsert_space(svc, vid, level_id, sp)
        space_by_ext[sp["external_id"]] = space.id
        ids["space_ids"].append(space.id)
        if primary_space_id is None:
            primary_space_id = space.id

    disc_by_code: dict[str, str] = {}
    for d in proposal.get("disciplines") or []:
        disc = _upsert_discipline(svc, vid, d)
        disc_by_code[disc.code] = disc.id
        ids["discipline_ids"].append(disc.id)

    element_by_ext: dict[str, str] = {}
    for el in proposal.get("elements") or []:
        created_el = _upsert_element(
            svc,
            vid,
            el,
            level_id=level_id,
            space_id=primary_space_id if el.get("attach_space") else None,
            discipline_id=disc_by_code.get(el.get("discipline_code") or "")
            if el.get("attach_discipline")
            else None,
        )
        element_by_ext[el["external_id"]] = created_el.id
        ids["element_ids"].append(created_el.id)
        # Params embebidos en element proposal
        if el.get("params"):
            ps = svc.upsert_parameter_set(
                vid,
                schemas.ParameterSetUpsert(
                    owner_kind="element",
                    owner_id=created_el.id,
                    code="perception",
                    external_id=f"{el['external_id']}:params",
                    display_name=f"Params {el.get('display_name')}",
                    data={
                        "params": el["params"],
                        "metadata": {"source": "perception"},
                    },
                ),
            )
            ids["parameter_set_ids"].append(ps.id)

    for ps_spec in proposal.get("parameter_sets") or []:
        owner_kind, owner_id = _resolve_owner(
            ps_spec.get("owner_ref"),
            site_id=site_id,
            element_by_ext=element_by_ext,
        )
        if not owner_id:
            continue
        ps = svc.upsert_parameter_set(
            vid,
            schemas.ParameterSetUpsert(
                owner_kind=owner_kind,
                owner_id=owner_id,
                code="perception",
                external_id=ps_spec.get("external_id"),
                display_name=ps_spec.get("display_name"),
                data=ps_spec.get("data") or {"params": {}, "metadata": {}},
            ),
        )
        ids["parameter_set_ids"].append(ps.id)

    return ids


def _resolve_owner(
    owner_ref: Optional[str],
    *,
    site_id: Optional[str],
    element_by_ext: dict[str, str],
) -> tuple[str, Optional[str]]:
    ref = owner_ref or ""
    if ref == "site":
        return "site", site_id
    if ref.startswith("element:"):
        key = ref.split(":", 1)[1]
        # proposal uses owner_ref "element:wall" → match external ending
        for ext, eid in element_by_ext.items():
            if ext.endswith(f":element:{key}") or ext.endswith(f":{key}"):
                return "element", eid
        # fallback: first element
        if element_by_ext:
            return "element", next(iter(element_by_ext.values()))
    return "element", None


def _upsert_site(svc: MdoService, version_id: str, spec: dict):
    existing = _find_by_external(svc, Site, version_id, spec["external_id"])
    if existing:
        return svc.update_site(
            existing.id,
            schemas.SiteUpdate(
                code=spec.get("code"),
                display_name=spec["display_name"],
                external_id=spec.get("external_id"),
                lot_ref=spec.get("lot_ref"),
                area_m2=spec.get("area_m2"),
            ),
        )
    return svc.create_site(
        version_id,
        schemas.SiteCreate(
            code=spec.get("code"),
            display_name=spec["display_name"],
            external_id=spec.get("external_id"),
            lot_ref=spec.get("lot_ref"),
            area_m2=spec.get("area_m2"),
        ),
    )


def _upsert_building(svc: MdoService, version_id: str, site_id: str, spec: dict):
    existing = _find_by_external(svc, Building, version_id, spec["external_id"])
    if existing:
        return svc.update_building(
            existing.id,
            schemas.BuildingUpdate(
                code=spec.get("code"),
                display_name=spec["display_name"],
                external_id=spec.get("external_id"),
                typology=spec.get("typology"),
            ),
        )
    return svc.create_building(
        version_id,
        schemas.BuildingCreate(
            site_id=site_id,
            code=spec.get("code"),
            display_name=spec["display_name"],
            external_id=spec.get("external_id"),
            typology=spec.get("typology"),
        ),
    )


def _upsert_level(svc: MdoService, version_id: str, building_id: str, spec: dict):
    existing = _find_by_external(svc, Level, version_id, spec["external_id"])
    if existing:
        return svc.update_level(
            existing.id,
            schemas.LevelUpdate(
                code=spec.get("code"),
                display_name=spec["display_name"],
                external_id=spec.get("external_id"),
                elevation_m=spec.get("elevation_m"),
                sort_order=spec.get("sort_order"),
            ),
        )
    return svc.create_level(
        version_id,
        schemas.LevelCreate(
            building_id=building_id,
            code=spec.get("code"),
            display_name=spec["display_name"],
            external_id=spec.get("external_id"),
            elevation_m=spec.get("elevation_m"),
            sort_order=spec.get("sort_order") or 0,
        ),
    )


def _upsert_space(svc: MdoService, version_id: str, level_id: str, spec: dict):
    existing = _find_by_external(svc, Space, version_id, spec["external_id"])
    if existing:
        return svc.update_space(
            existing.id,
            schemas.SpaceUpdate(
                code=spec.get("code"),
                display_name=spec["display_name"],
                external_id=spec.get("external_id"),
                space_type=spec.get("space_type"),
                area_m2=spec.get("area_m2"),
            ),
        )
    return svc.create_space(
        version_id,
        schemas.SpaceCreate(
            level_id=level_id,
            code=spec.get("code"),
            display_name=spec["display_name"],
            external_id=spec.get("external_id"),
            space_type=spec.get("space_type"),
            area_m2=spec.get("area_m2"),
        ),
    )


def _upsert_discipline(svc: MdoService, version_id: str, spec: dict):
    existing = _find_by_external(svc, Discipline, version_id, spec["external_id"])
    if existing:
        return svc.update_discipline(
            existing.id,
            schemas.DisciplineUpdate(
                display_name=spec["display_name"],
                external_id=spec.get("external_id"),
                description=spec.get("description"),
            ),
        )
    # code unique per version — if soft-deleted conflict, create may fail; try by code
    by_code = (
        svc.db.query(Discipline)
        .filter(
            Discipline.version_id == version_id,
            Discipline.code == spec["code"],
            Discipline.deleted_at.is_(None),
            Discipline.studio_id == svc.studio_id,
        )
        .first()
    )
    if by_code:
        return by_code
    return svc.create_discipline(
        version_id,
        schemas.DisciplineCreate(
            code=spec["code"],
            display_name=spec["display_name"],
            external_id=spec.get("external_id"),
            description=spec.get("description"),
        ),
    )


def _upsert_element(
    svc: MdoService,
    version_id: str,
    spec: dict,
    *,
    level_id: Optional[str],
    space_id: Optional[str],
    discipline_id: Optional[str],
):
    existing = _find_by_external(svc, Element, version_id, spec["external_id"])
    if existing:
        return svc.update_element(
            existing.id,
            schemas.ElementUpdate(
                discipline_code=spec["discipline_code"],
                element_type=spec["element_type"],
                display_name=spec["display_name"],
                code=spec.get("code"),
                external_id=spec.get("external_id"),
                level_id=level_id,
                space_id=space_id,
                discipline_id=discipline_id,
            ),
        )
    return svc.create_element(
        version_id,
        schemas.ElementCreate(
            discipline_code=spec["discipline_code"],
            element_type=spec["element_type"],
            display_name=spec["display_name"],
            code=spec.get("code"),
            external_id=spec.get("external_id"),
            level_id=level_id,
            space_id=space_id,
            discipline_id=discipline_id,
        ),
    )
