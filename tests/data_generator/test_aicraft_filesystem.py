import json
from unittest.mock import MagicMock, mock_open, patch

import pytest

from data_generator.generators.aircraft_generator import AircraftGenerator


@pytest.fixture
def generator():
    return AircraftGenerator()


def create_fake_vehicle(vin="TESTVIN123"):
    vehicle = MagicMock()
    vehicle.vin = vin
    return vehicle


@patch("data_generator.generators.aircraft_generator.asdict", return_value={"vin": "x"})
@patch("data_generator.generators.aircraft_generator.json.dump")
@patch("data_generator.generators.aircraft_generator.open", new_callable=mock_open)
def test_to_json_creates_one_file_per_vehicle(
    mock_file, mock_json_dump, mock_asdict, generator
):
    vehicles = [create_fake_vehicle("VIN1"), create_fake_vehicle("VIN2")]

    generator.to_json(vehicles, path=MagicMock())

    assert mock_file.call_count == len(vehicles)
    assert mock_json_dump.call_count == len(vehicles)


@patch("data_generator.generators.aircraft_generator.Path.mkdir")
@patch("data_generator.generators.aircraft_generator.open", new_callable=mock_open)
@patch("data_generator.generators.aircraft_generator.json.dump")
def test_mkdir_called_with_correct_args(
    mock_json_dump, mock_file, mock_mkdir, generator
):
    vehicles = [create_fake_vehicle()]

    fake_path = MagicMock()
    fake_file_path = MagicMock()
    fake_file_path.parent = MagicMock()

    fake_path.__truediv__.return_value = fake_file_path

    generator.to_json(vehicles, path=fake_path)

    fake_file_path.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)


@patch("data_generator.generators.aircraft_generator.open", new_callable=mock_open)
@patch("data_generator.generators.aircraft_generator.json.dump")
def test_custom_path_overrides_base_path(mock_json_dump, mock_file, generator):
    vehicles = [create_fake_vehicle()]

    custom_path = MagicMock()
    fake_file_path = MagicMock()
    custom_path.__truediv__.return_value = fake_file_path
    fake_file_path.parent = MagicMock()

    generator.to_json(vehicles, path=custom_path)

    custom_path.__truediv__.assert_called()


@patch("data_generator.generators.aircraft_generator.open", new_callable=mock_open)
@patch("data_generator.generators.aircraft_generator.json.dump")
def test_uses_base_path_when_none(mock_json_dump, mock_file, generator):
    vehicles = [create_fake_vehicle()]

    generator.base_path = MagicMock()
    fake_file_path = MagicMock()
    generator.base_path.__truediv__.return_value = fake_file_path
    fake_file_path.parent = MagicMock()

    generator.to_json(vehicles, path=None)

    generator.base_path.__truediv__.assert_called()


@patch("data_generator.generators.aircraft_generator.open", new_callable=mock_open)
def test_written_content_is_valid_json(mock_file, generator):
    vehicle = create_fake_vehicle()

    data = {"vin": "TESTVIN123"}
    with patch(
        "data_generator.generators.aircraft_generator.asdict", return_value=data
    ):
        generator.to_json([vehicle], path=MagicMock())

    handle = mock_file()
    written = "".join(call.args[0] for call in handle.write.call_args_list)

    parsed = json.loads(written)

    assert parsed == data
