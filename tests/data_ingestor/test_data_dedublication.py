import pytest

from data_ingestor.vehicle_processor import VehicleProcessor


@pytest.fixture
def sample_aircraft_dict():
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


@pytest.fixture
def transformer():
    return VehicleProcessor()


def test_two_diff_vins(sample_aircraft_dict, transformer):
    copy_aircraft = sample_aircraft_dict.copy()
    # First vehicle
    expected_result: str = '{"type": "aircraft", "vin": "AIR-6873-TJH", "brand": "Bombardier", "model": "737 Max", "metadata_year": 2023, "metadata_factory": "Wichita Facility", "technical_specs_engine_type": "Turbofan", "technical_specs_engine_horsepower": 19767, "technical_specs_max_altitude": 21814, "features_0": "school", "features_1": "American", "features_2": "of", "content": "This aircraft is a Bombardier 737 Max manufactured in 2023. It has a Turbofan engine with 19767 horsepower.Also it has a 21814 maximal altitude.This aircraft has a features like: school, American, of."}'
    result = transformer.process(copy_aircraft)
    assert result == expected_result

    # Second vehicle
    copy_aircraft["vin"] = "YYYYXXX223"
    second_expected_result: str = '{"type": "aircraft", "vin": "YYYYXXX223", "brand": "Bombardier", "model": "737 Max", "metadata_year": 2023, "metadata_factory": "Wichita Facility", "technical_specs_engine_type": "Turbofan", "technical_specs_engine_horsepower": 19767, "technical_specs_max_altitude": 21814, "features_0": "school", "features_1": "American", "features_2": "of", "content": "This aircraft is a Bombardier 737 Max manufactured in 2023. It has a Turbofan engine with 19767 horsepower.Also it has a 21814 maximal altitude.This aircraft has a features like: school, American, of."}'

    result = transformer.process(copy_aircraft)
    assert result == second_expected_result


def test_two_same_vins(sample_aircraft_dict, transformer):
    copy_aircraft = sample_aircraft_dict.copy()
    # First vehicle
    expected_result: str = '{"type": "aircraft", "vin": "AIR-6873-TJH", "brand": "Bombardier", "model": "737 Max", "metadata_year": 2023, "metadata_factory": "Wichita Facility", "technical_specs_engine_type": "Turbofan", "technical_specs_engine_horsepower": 19767, "technical_specs_max_altitude": 21814, "features_0": "school", "features_1": "American", "features_2": "of", "content": "This aircraft is a Bombardier 737 Max manufactured in 2023. It has a Turbofan engine with 19767 horsepower.Also it has a 21814 maximal altitude.This aircraft has a features like: school, American, of."}'
    result = transformer.process(copy_aircraft)
    assert result == expected_result

    # Second vehicle
    result = transformer.process(copy_aircraft)
    assert result is None
