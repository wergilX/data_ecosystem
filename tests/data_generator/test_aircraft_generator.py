import pytest

from data_generator.generators.aircraft_generator import AircraftGenerator


@pytest.fixture
def aircraft_gen():
    """Create fixture for aircraft"""
    return AircraftGenerator()


@pytest.mark.parametrize("count", [1, 50, 100])
def test_aircraft_generator_create_aircraft(aircraft_gen, count):
    data = aircraft_gen.generate(count)
    assert isinstance(data, list)
    assert len(data) == count

    for item in data:
        assert item.type == "aircraft"

        assert isinstance(item.vin, str)
        assert item.vin.isupper()

        assert item.brand is not None
        assert item.model is not None

        assert isinstance(item.metadata.year, int)
        assert item.metadata.year >= 1990
        assert item.metadata.factory is not None

        assert item.technical_specs.engine.type is not None
        assert item.technical_specs.engine.horsepower >= 150
        assert item.technical_specs.max_altitude >= 10000

        assert isinstance(item.features, list)


@pytest.mark.parametrize("count", [1, 10])
def test_aircraft_generator_create_dict_aircrafts(aircraft_gen, count):
    data = aircraft_gen.generate(count)
    assert isinstance(data, list)
    assert len(data) == count

    for item in data:
        dict_item = item.to_dict()
        assert isinstance(dict_item, dict)

        expected_keys = {
            "type",
            "vin",
            "brand",
            "model",
            "metadata",
            "technical_specs",
            "features",
        }
        assert expected_keys.issubset(dict_item.keys()), (
            f"Missing keys in {item.keys()}"
        )


@pytest.mark.parametrize("count", [1, 5, 10])
def test_aircraft_generator_save_file(aircraft_gen, count, tmp_path):
    data = aircraft_gen.generate(count)
    assert isinstance(data, list)
    assert len(data) == count

    aircraft_gen.to_json(data, tmp_path)

    json_files_count = len(list(tmp_path.glob("*.json")))

    assert tmp_path.exists()
    assert json_files_count == count
