"""Enums abiertos / estados del MDO.

Element tipado NO usa un enum monolítico de tipologías.
La separación disciplina vs tipo concreto vive en `typing_rules`.
"""

from __future__ import annotations

from enum import Enum


class VersionStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SEALED = "sealed"


MUTABLE_VERSION_STATUSES = frozenset({VersionStatus.DRAFT.value, VersionStatus.ACTIVE.value})


class ParameterOwnerKind(str, Enum):
    SITE = "site"
    BUILDING = "building"
    LEVEL = "level"
    SPACE = "space"
    DISCIPLINE = "discipline"
    ELEMENT = "element"


class DomainEventType(str, Enum):
    VERSION_ENSURED = "mdo.version.ensured"
    VERSION_SEALED = "mdo.version.sealed"
    SITE_CREATED = "mdo.site.created"
    SITE_UPDATED = "mdo.site.updated"
    SITE_DELETED = "mdo.site.deleted"
    BUILDING_CREATED = "mdo.building.created"
    BUILDING_UPDATED = "mdo.building.updated"
    BUILDING_DELETED = "mdo.building.deleted"
    LEVEL_CREATED = "mdo.level.created"
    LEVEL_UPDATED = "mdo.level.updated"
    LEVEL_DELETED = "mdo.level.deleted"
    SPACE_CREATED = "mdo.space.created"
    SPACE_UPDATED = "mdo.space.updated"
    SPACE_DELETED = "mdo.space.deleted"
    DISCIPLINE_CREATED = "mdo.discipline.created"
    DISCIPLINE_UPDATED = "mdo.discipline.updated"
    DISCIPLINE_DELETED = "mdo.discipline.deleted"
    ELEMENT_CREATED = "mdo.element.created"
    ELEMENT_UPDATED = "mdo.element.updated"
    ELEMENT_DELETED = "mdo.element.deleted"
    PARAMETER_SET_UPSERTED = "mdo.parameter_set.upserted"
    PARAMETER_SET_DELETED = "mdo.parameter_set.deleted"
