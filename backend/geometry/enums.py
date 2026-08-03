"""Enums / constantes del dominio Geometry."""

from __future__ import annotations

from enum import Enum


class GeomType(str, Enum):
    VERTICAL_SURFACE = "vertical_surface"
    HORIZONTAL_REGION = "horizontal_region"
    LINEAR_RUN = "linear_run"
    OPENING = "opening"
    LOT_REGION = "lot_region"
    UNKNOWN = "unknown"


class MeasureSource(str, Enum):
    MDO_PARAMS = "mdo_params"
    MDO_COLUMN = "mdo_column"
    COMPUTED = "computed"
    UNAVAILABLE = "unavailable"


class IssueSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class IssueSource(str, Enum):
    VALIDATOR = "validator"
    COMPUTE = "compute"
    INGEST = "ingest"


# Tolerancia relativa area vs length*height cuando length es derived
DEFAULT_AREA_TOLERANCE_RATIO = 0.05

EVENT_COMPUTE_STARTED = "geometry.compute.started"
EVENT_COMPUTE_COMPLETED = "geometry.compute.completed"
EVENT_COMPUTE_FAILED = "geometry.compute.failed"
EVENT_ELEMENT_UPSERTED = "geometry.element.upserted"
EVENT_ISSUE_RAISED = "geometry.issue.raised"
