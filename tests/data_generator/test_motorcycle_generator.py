import pytest

from data_generator.generators.motorcycle_generator import MotorcycleGenerator


@pytest.fixture
def motorcycle_gen():
    """Create fixture for motorcycle"""
    return MotorcycleGenerator()


@pytest.mark.parametrize("count", [1, 50, 100])
def test_motorcycle_generator_create_motorcycle(motorcycle_gen, count):
    data = motorcycle_gen.generate(count)
    assert isinstance(data, list)
    assert len(data) == count

    for item in data:
        assert item.type == "motorcycle"

        assert isinstance(item.vin, str)
        assert item.vin.isupper()

        assert item.brand is not None
        assert item.model is not None

        assert isinstance(item.metadata.year, int)
        assert item.metadata.year >= 2015
        assert item.metadata.factory is not None

        assert item.technical_specs.engine.type is not None
        assert item.technical_specs.engine.horsepower >= 50

        assert isinstance(item.features, list)


@pytest.mark.parametrize("count", [1, 10])
def test_motorcycle_generator_create_dict_motorcycle(motorcycle_gen, count):
    data = motorcycle_gen.generate(count)
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
            "has_sidecar",
            "metadata",
            "technical_specs",
            "features",
        }
        assert expected_keys.issubset(dict_item.keys()), (
            f"Missing keys in {item.keys()}"
        )


@pytest.mark.parametrize("count", [1, 5, 10])
def test_motorcycle_generator_save_file(motorcycle_gen, count, tmp_path):
    data = motorcycle_gen.generate(count)
    assert isinstance(data, list)
    assert len(data) == count

    motorcycle_gen.to_json(data, tmp_path)

    json_files_count = len(list(tmp_path.glob("*.json")))

    assert tmp_path.exists()
    assert json_files_count == count
