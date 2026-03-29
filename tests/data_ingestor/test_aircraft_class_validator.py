import pytest
from pydantic import ValidationError

from data_ingestor.entities.aircraft import Aircraft
from data_ingestor.exceptions import HorspowerError, VinError, YearError


@pytest.fixture
def sample_aircraft_dict():
    """Create aircraft dict"""
    return {
        "type": "aircraft",
        "vin": "AIR-6873-TJH",
        "brand": "Bombardier",
        "model": "737 Max",
        "metadata": {"year": 2023, "factory": "Wichita Facility"},
        "technical_specs": {
            "engine": {"type": "Turbofan", "horsepower": 19767},
            "max_altitude": 21814,
        },
        "features": ["school", "American", "of"],
    }


def test_aircraft_validate_data(sample_aircraft_dict):
    assert Aircraft.model_validate(sample_aircraft_dict)


def test_aircraft_missing_vin(sample_aircraft_dict):
    test_data = sample_aircraft_dict.copy()
    test_data.pop("vin")

    with pytest.raises(ValidationError) as exc_info:
        Aircraft.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("vin",)
    assert errors[0]["type"] == "missing"


def test_aircraft_invalid_vin(sample_aircraft_dict):
    test_data = sample_aircraft_dict.copy()
    test_data["vin"] = ""

    with pytest.raises(VinError):
        Aircraft.model_validate(test_data)


def test_aircraft_invalid_hp(sample_aircraft_dict):
    test_data = sample_aircraft_dict.copy()
    test_data["technical_specs"]["engine"]["horsepower"] = -20

    with pytest.raises(HorspowerError):
        Aircraft.model_validate(test_data)


def test_aircraft_invalid_year_str(sample_aircraft_dict):
    test_data = sample_aircraft_dict.copy()
    test_data["metadata"]["year"] = "test string"

    with pytest.raises(ValidationError) as exc_info:
        Aircraft.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("metadata", "year")


def test_aircraft_invalid_year(sample_aircraft_dict):
    test_data = sample_aircraft_dict.copy()
    test_data["metadata"]["year"] = -20

    with pytest.raises(YearError):
        Aircraft.model_validate(test_data)


def test_aircraft_extra_field(sample_aircraft_dict):
    test_data = sample_aircraft_dict.copy()
    test_data["unknown"] = "ERROR"

    with pytest.raises(ValidationError) as exc_info:
        Aircraft.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == ("unknown",)


def test_aircraft_empty_dict():
    test_data = {}

    with pytest.raises(ValidationError) as exc_info:
        Aircraft.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["type"] == "missing"


def test_aircraft_missing_nested_value(sample_aircraft_dict):
    test_data = sample_aircraft_dict.copy()
    test_data["technical_specs"]["engine"].pop("type")

    with pytest.raises(ValidationError) as exc_info:
        Aircraft.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == (
        "technical_specs",
        "engine",
        "type",
    )
    assert errors[0]["type"] == "missing"


def test_aircraft_missing_max_altitude(sample_aircraft_dict):
    test_data = sample_aircraft_dict.copy()
    test_data["technical_specs"].pop("max_altitude")

    with pytest.raises(ValidationError) as exc_info:
        Aircraft.model_validate(test_data)

    errors = exc_info.value.errors()
    assert errors[0]["loc"] == (
        "technical_specs",
        "max_altitude",
    )
    assert errors[0]["type"] == "missing"
