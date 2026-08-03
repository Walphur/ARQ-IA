"""Mapper puro Perception detections → propuestas MDO (sin I/O, sin precios).

E03-F01: Building / Level / Space / Element.
No importa motor_ia ni calcula materiales/costos.
"""

from __future__ import annotations

from typing import Any, Optional


def wall_element_type(sistema_muro: Optional[str]) -> str:
    s = (sistema_muro or "").lower()
    if "retak" in s:
        return "wall.retak"
    if "steel" in s or "steel_frame" in s:
        return "wall.steel_frame"
    if "drywall" in s or "yeso" in s:
        return "wall.drywall"
    if "comun" in s or "macizo" in s:
        return "wall.masonry.brick"
    return "wall.masonry.brick"


def map_detections_to_mdo_proposal(
    detections: dict[str, Any],
    *,
    process_id: int,
    project_name: str = "Obra",
) -> dict[str, Any]:
    """Convierte `detections` del motor en un plan de entidades MDO.

    Retorna estructura serializable (sin side-effects).
    `external_id` usa prefijo `process:{id}:…` para strangler idempotente.
    """
    if not isinstance(detections, dict):
        raise ValueError("detections debe ser un dict.")
    tipo = str(detections.get("tipo_plano") or "muros")
    facts = detections.get("facts") or {}
    if not isinstance(facts, dict):
        facts = {}
    prefix = f"process:{process_id}"
    sistema = detections.get("sistema_muro")
    altura = detections.get("altura_muro_m")

    proposal: dict[str, Any] = {
        "schema_version": "1",
        "process_id": process_id,
        "tipo_plano": tipo,
        "site": None,
        "building": None,
        "level": None,
        "spaces": [],
        "disciplines": [],
        "elements": [],
        "parameter_sets": [],
    }

    if tipo == "terreno":
        lots = facts.get("lots") or []
        if lots:
            first = lots[0]
            proposal["site"] = {
                "external_id": f"{prefix}:site",
                "code": "SITE",
                "display_name": f"Lote / terreno — {project_name}",
                "area_m2": first.get("area_m2"),
                "lot_ref": f"lote-{first.get('lot_number', 1)}",
            }
            # Solo Site para terreno en F01 (sin Building/Element de costos).
            proposal["parameter_sets"].append(
                {
                    "owner_ref": "site",
                    "external_id": f"{prefix}:params:site",
                    "display_name": "Params lote (percepción)",
                    "data": {
                        "params": {
                            "lots": lots,
                            "perimeter_m": first.get("perimeter_m"),
                        },
                        "metadata": {"source": "perception", "tipo_plano": tipo},
                    },
                }
            )
        return proposal

    # Estructura espacial mínima para planos de obra
    proposal["site"] = {
        "external_id": f"{prefix}:site",
        "code": "SITE",
        "display_name": f"Sitio — {project_name}",
        "area_m2": facts.get("floor_area_m2") or facts.get("roof_area_m2"),
    }
    proposal["building"] = {
        "external_id": f"{prefix}:building",
        "code": "B1",
        "display_name": f"Edificio — {project_name}",
        "typology": "detected",
    }
    proposal["level"] = {
        "external_id": f"{prefix}:level",
        "code": "PB",
        "display_name": "Planta baja",
        "elevation_m": 0.0,
        "sort_order": 0,
    }

    if tipo == "muros":
        proposal["disciplines"].append(
            {
                "external_id": f"{prefix}:discipline:architecture",
                "code": "architecture",
                "display_name": "Arquitectura",
            }
        )
        floor_area = facts.get("floor_area_m2")
        proposal["spaces"].append(
            {
                "external_id": f"{prefix}:space:detected-floor",
                "code": "SP-FLOOR",
                "display_name": "Espacio detectado (pisos)",
                "space_type": "space.room",
                "area_m2": floor_area,
            }
        )
        wall_type = wall_element_type(str(sistema) if sistema else None)
        proposal["elements"].append(
            {
                "external_id": f"{prefix}:element:wall",
                "code": "WALL",
                "display_name": "Muros detectados",
                "discipline_code": "architecture",
                "element_type": wall_type,
                "attach_space": True,
                "attach_discipline": True,
            }
        )
        openings = int(facts.get("openings_count") or 0)
        if openings > 0:
            proposal["elements"].append(
                {
                    "external_id": f"{prefix}:element:openings",
                    "code": "OPEN",
                    "display_name": f"Aberturas detectadas ({openings})",
                    "discipline_code": "architecture",
                    "element_type": "opening.door",
                    "attach_space": True,
                    "attach_discipline": True,
                    "params": {"openings_count": openings},
                }
            )
        if floor_area and float(floor_area) > 0:
            proposal["elements"].append(
                {
                    "external_id": f"{prefix}:element:floor",
                    "code": "FLOOR",
                    "display_name": "Pisos detectados",
                    "discipline_code": "architecture",
                    "element_type": "floor.carpetas",
                    "attach_space": True,
                    "attach_discipline": True,
                }
            )
        proposal["parameter_sets"].append(
            {
                "owner_ref": "element:wall",
                "external_id": f"{prefix}:params:wall",
                "display_name": "Params muro (percepción)",
                "data": {
                    "params": {
                        "wall_face_area_m2": facts.get("wall_face_area_m2"),
                        "wall_height_m": facts.get("wall_height_m") or altura,
                        "sistema_muro": sistema,
                    },
                    "metadata": {"source": "perception", "tipo_plano": tipo},
                },
            }
        )

    elif tipo == "agua":
        proposal["disciplines"].append(
            {
                "external_id": f"{prefix}:discipline:plumbing",
                "code": "plumbing",
                "display_name": "Sanitarias",
            }
        )
        proposal["spaces"].append(
            {
                "external_id": f"{prefix}:space:installations",
                "code": "SP-INST",
                "display_name": "Nivel instalaciones",
                "space_type": "space.room",
                "area_m2": None,
            }
        )
        proposal["elements"].append(
            {
                "external_id": f"{prefix}:element:plumbing",
                "code": "PLUMB",
                "display_name": "Red de agua/cloaca detectada",
                "discipline_code": "plumbing",
                "element_type": "generic.element",
                "attach_space": True,
                "attach_discipline": True,
                "params": {
                    "cold_water_ml": facts.get("cold_water_ml"),
                    "hot_water_ml": facts.get("hot_water_ml"),
                    "sewage_ml": facts.get("sewage_ml"),
                    "water_outlets": facts.get("water_outlets"),
                },
            }
        )

    elif tipo == "luz":
        proposal["disciplines"].append(
            {
                "external_id": f"{prefix}:discipline:electrical",
                "code": "electrical",
                "display_name": "Eléctrica",
            }
        )
        proposal["spaces"].append(
            {
                "external_id": f"{prefix}:space:electrical",
                "code": "SP-ELEC",
                "display_name": "Nivel eléctrica",
                "space_type": "space.room",
                "area_m2": None,
            }
        )
        proposal["elements"].append(
            {
                "external_id": f"{prefix}:element:electrical",
                "code": "ELEC",
                "display_name": "Instalación eléctrica detectada",
                "discipline_code": "electrical",
                "element_type": "generic.element",
                "attach_space": True,
                "attach_discipline": True,
                "params": {
                    "electrical_conduit_ml": facts.get("electrical_conduit_ml"),
                    "electrical_boxes_count": facts.get("electrical_boxes_count"),
                },
            }
        )

    elif tipo == "techo":
        proposal["disciplines"].append(
            {
                "external_id": f"{prefix}:discipline:envelope",
                "code": "envelope",
                "display_name": "Envolvente",
            }
        )
        proposal["spaces"].append(
            {
                "external_id": f"{prefix}:space:roof",
                "code": "SP-ROOF",
                "display_name": "Cubierta",
                "space_type": "space.room",
                "area_m2": facts.get("roof_area_m2"),
            }
        )
        proposal["elements"].append(
            {
                "external_id": f"{prefix}:element:roof",
                "code": "ROOF",
                "display_name": "Techo detectado",
                "discipline_code": "envelope",
                "element_type": "roof.metal",
                "attach_space": True,
                "attach_discipline": True,
                "params": {"roof_area_m2": facts.get("roof_area_m2")},
            }
        )

    else:
        # tipo desconocido: skeleton espacial vacío + element genérico
        proposal["disciplines"].append(
            {
                "external_id": f"{prefix}:discipline:other",
                "code": "other",
                "display_name": "Otra",
            }
        )
        proposal["elements"].append(
            {
                "external_id": f"{prefix}:element:generic",
                "code": "GEN",
                "display_name": f"Detección {tipo}",
                "discipline_code": "other",
                "element_type": "generic.element",
                "attach_discipline": True,
                "params": {"facts": facts},
            }
        )

    return proposal
