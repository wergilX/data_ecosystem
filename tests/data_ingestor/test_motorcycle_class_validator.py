import pytest
from pydantic import ValidationError

from data_ingestor.schemas.motorcycle import Motorcycle


@pytest.fixture
def sample_motorcycle_dict():
    return {
        "type": "motorcycle",
        "vin": "MOT827TGW",
        "brand": "Harley-Davidson",
        "model": "Monster",
        "has_sidecar": False,
        "metadata": {"year": 2020, "factory": "Bologna Plant"},
        "technical_specs": {"engine": {"type": "Boxer", "horsepower": 133}},
        "features": ["administration"],
    }


def test_validate_motorcycle_data(sample_motorcycle_dict):
    assert Motorcycle.model_validate(sample_motorcycle_dict)


def test_missing_vin(sample_motorcycle_dict):
    test_data = sample_motorcycle_dict.copy()
    test_data.pop("vin")

    with pytest.raises(ValidationError) as exc_info:
        Motorcycle.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("vin",)
    assert errors[0]["type"] == "missing"


def test_motorcycle_invalid_vin(sample_motorcycle_dict):
    test_data = sample_motorcycle_dict.copy()
    test_data["vin"] = ""

    with pytest.raises(ValidationError):
        Motorcycle.model_validate(test_data)


def test_motorcycle_invalid_hp(sample_motorcycle_dict):
    test_data = sample_motorcycle_dict.copy()
    test_data["technical_specs"]["engine"]["horsepower"] = -20

    with pytest.raises(ValidationError):
        Motorcycle.model_validate(test_data)


def test_motorcycle_invalid_year_str(sample_motorcycle_dict):
    test_data = sample_motorcycle_dict.copy()
    test_data["metadata"]["year"] = "test string"

    with pytest.raises(ValidationError) as exc_info:
        Motorcycle.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("metadata", "year")


def test_motorcycle_invalid_year(sample_motorcycle_dict):
    test_data = sample_motorcycle_dict.copy()
    test_data["metadata"]["year"] = -20

    with pytest.raises(ValidationError):
        Motorcycle.model_validate(test_data)


def test_motorcycle_extra_field(sample_motorcycle_dict):
    test_data = sample_motorcycle_dict.copy()
    test_data["unknown"] = "ERROR"

    with pytest.raises(ValidationError) as exc_info:
        Motorcycle.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("unknown",)


def test_motorcycle_empty_dict():
    test_data = {}

    with pytest.raises(ValidationError) as exc_info:
        Motorcycle.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["type"] == "missing"


def test_motorcycle_missing_nested_value(sample_motorcycle_dict):
    test_data = sample_motorcycle_dict.copy()
    test_data["technical_specs"]["engine"].pop("type")

    with pytest.raises(ValidationError) as exc_info:
        Motorcycle.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == (
        "technical_specs",
        "engine",
        "type",
    )
    assert errors[0]["type"] == "missing"


def test_motorcycle_missing_sidecar_value(sample_motorcycle_dict):
    test_data = sample_motorcycle_dict.copy()
    test_data.pop("has_sidecar")

    with pytest.raises(ValidationError) as exc_info:
        Motorcycle.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("has_sidecar",)
    assert errors[0]["type"] == "missing"
