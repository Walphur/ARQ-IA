"""Fase 1 — reglas ParameterSet + clasificación Element."""

import pytest

from mdo.typing_rules import (
    MdoValidationError,
    normalize_parameter_set_data,
    validate_element_classification,
)


def test_parameter_set_allows_params_and_metadata_only():
    data = normalize_parameter_set_data(
        {"params": {"thickness_m": 0.15}, "metadata": {"source": "manual"}}
    )
    assert data["params"]["thickness_m"] == 0.15
    assert data["metadata"]["source"] == "manual"


def test_parameter_set_rejects_structural_root_keys():
    with pytest.raises(MdoValidationError, match="solo admite"):
        normalize_parameter_set_data({"level_id": "x", "params": {}})


def test_parameter_set_rejects_structural_nested_keys():
    with pytest.raises(MdoValidationError, match="hechos estructurales"):
        normalize_parameter_set_data({"params": {"element_type": "wall.x"}, "metadata": {}})


def test_parameter_set_rejects_geometry_in_metadata():
    with pytest.raises(MdoValidationError, match="hechos estructurales"):
        normalize_parameter_set_data({"params": {}, "metadata": {"geometry": {"x": 1}}})


def test_element_requires_dotted_concrete_type():
    with pytest.raises(MdoValidationError, match="concreto"):
        validate_element_classification("architecture", "WALL")


def test_element_separates_discipline_and_type():
    d, t = validate_element_classification("Architecture", "wall.masonry.brick")
    assert d == "architecture"
    assert t == "wall.masonry.brick"
