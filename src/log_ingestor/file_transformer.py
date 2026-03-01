import json
from pathlib import Path

from .car import Car


def read_data(file: Path) -> list[dict]:
    with open(file, "r") as json_file:
        raw_data = json.load(json_file)
        if not isinstance(raw_data, list):
            raise ValueError("JSON should have list type")
        return raw_data


def file_transformer(file_input: str, file_output: str):
    file = Path(file_input)
    if not file.exists():
        raise ValueError(f"Wrong path {file_input}")

    raw_data = read_data(file)

    try:
        cars = [Car.model_validate(item) for item in raw_data]
        write_data(file_output, cars)
    except Exception as e:
        print(f"Error validation: {e}")


def write_data(file_output: str, cars: list[Car]):
    file = Path(file_output)
    file.parent.mkdir(parents=True, exist_ok=True)

    for car in cars:
        with open(file, "a") as json_file:
            json.dump(
                car.model_dump(),
                json_file,
            )
            json_file.write("\n")
