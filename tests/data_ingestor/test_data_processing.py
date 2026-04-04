import pytest

from data_ingestor.vehicle_processor import VehicleProcessor


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


@pytest.fixture
def transformer(tmp_path):
    return VehicleProcessor()


def test_one_level_dict(transformer):
    dummy_car = {
        "type": "car",
        "vin": "XAA954UUK",
        "brand": "Ford",
    }
    expected_result: str = '{"type": "car", "vin": "XAA954UUK", "brand": "Ford"}'
    result = transformer.to_flat_str(dummy_car)
    assert result == expected_result


def test_two_level_dict(transformer):
    dummy_car = {
        "metadata": {"year": 2024},
    }
    expected_result: str = '{"metadata_year": 2024}'
    result = transformer.to_flat_str(dummy_car)
    assert result == expected_result


def test_high_level_dict(transformer):
    dummy_car = {
        "technical_specs": {"engine": {"type": "Hybrid", "horsepower": 455}},
    }
    expected_result: str = '{"technical_specs_engine_type": "Hybrid", "technical_specs_engine_horsepower": 455}'
    result = transformer.to_flat_str(dummy_car)
    assert result == expected_result


def test_empty_dict(transformer):
    dummy_car = {}
    expected_result: str = "{}"
    result = transformer.to_flat_str(dummy_car)
    assert result == expected_result


def test_list_in_dict(transformer):
    dummy_car = {
        "features": ["charge", "admit"],
    }
    expected_result: str = '{"features_0": "charge", "features_1": "admit"}'
    result = transformer.to_flat_str(dummy_car)
    assert result == expected_result


def test_transform_single_vehicle(transformer, sample_car_dict):
    result = transformer.process(sample_car_dict)
    assert result is not None
    assert isinstance(result, str)
    assert "XAA954UUK" in result
