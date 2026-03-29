import pytest

from data_generator.generators.car_generator import CarGenerator


@pytest.fixture
def car_gen():
    """Create fixture for car"""
    return CarGenerator()


@pytest.mark.parametrize("count", [1, 50, 100])
def test_car_generator_create_cars(car_gen, count):
    data = car_gen.generate(count)
    assert isinstance(data, list)
    assert len(data) == count

    for item in data:
        assert item.type == "car"

        assert isinstance(item.vin, str)
        assert item.vin.isupper()

        assert item.brand is not None
        assert item.model is not None

        assert isinstance(item.metadata.year, int)
        assert item.metadata.year >= 2020
        assert item.metadata.factory is not None

        assert item.technical_specs.engine.type is not None
        assert item.technical_specs.engine.horsepower >= 200

        assert isinstance(item.features, list)


@pytest.mark.parametrize("count", [1, 10])
def test_car_generator_create_dict_cars(car_gen, count):
    data = car_gen.generate(count)
    assert isinstance(data, list)
    assert len(data) == count

    for item in data:
        dict_item = item.to_dict()
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
def test_car_generator_save_file(car_gen, count, tmp_path):
    data = car_gen.generate(count)
    assert isinstance(data, list)
    assert len(data) == count

    car_gen.to_json(data, tmp_path)

    json_files_count = len(list(tmp_path.glob("*.json")))

    assert tmp_path.exists()
    assert json_files_count == count
