import pytest
from pydantic import ValidationError

from data_ingestor.schemas.car import Car


@pytest.fixture
def sample_car_dict():
    return {
        "type": "car",
        "vin": "XAA954UUK",
        "brand": "Ford",
        "model": "Model Y",
        "metadata": {"year": 2024, "factory": "Giga Berlin"},
        "technical_specs": {"engine": {"type": "Hybrid", "horsepower": 455}},
        "features": ["charge", "admit"],
    }


def test_validate_car_data(sample_car_dict):
    assert Car.model_validate(sample_car_dict)


def test_missing_vin(sample_car_dict):
    test_data = sample_car_dict.copy()
    test_data.pop("vin")

    with pytest.raises(ValidationError) as exc_info:
        Car.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("vin",)
    assert errors[0]["type"] == "missing"


def test_invalid_vin(sample_car_dict):
    test_data = sample_car_dict.copy()
    test_data["vin"] = ""

    with pytest.raises(ValidationError):
        Car.model_validate(test_data)


def test_invalid_hp(sample_car_dict):
    test_data = sample_car_dict.copy()
    test_data["technical_specs"]["engine"]["horsepower"] = -20

    with pytest.raises(ValidationError):
        Car.model_validate(test_data)


def test_car_invalid_year_str(sample_car_dict):
    test_data = sample_car_dict.copy()
    test_data["metadata"]["year"] = "test string"

    with pytest.raises(ValidationError) as exc_info:
        Car.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("metadata", "year")


def test_car_invalid_year(sample_car_dict):
    test_data = sample_car_dict.copy()
    test_data["metadata"]["year"] = -20

    with pytest.raises(ValidationError):
        Car.model_validate(test_data)


def test_car_extra_field(sample_car_dict):
    test_data = sample_car_dict.copy()
    test_data["unknown"] = "ERROR"

    with pytest.raises(ValidationError) as exc_info:
        Car.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("unknown",)


def test_empty_dict():
    test_data = {}

    with pytest.raises(ValidationError) as exc_info:
        Car.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["type"] == "missing"


def test_missing_nested_value(sample_car_dict):
    test_data = sample_car_dict.copy()
    test_data["technical_specs"]["engine"].pop("type")

    with pytest.raises(ValidationError) as exc_info:
        Car.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == (
        "technical_specs",
        "engine",
        "type",
    )
    assert errors[0]["type"] == "missing"
