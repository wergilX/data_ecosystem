import json
import logging
from pathlib import Path
from typing import Generator

from flatten_json import flatten

from .car import Car


class FileTransformer:
    def __init__(self):
        """Create container with processed vin"""
        self.processed_vins = set()

    def read_data(self, input_path: Path) -> list[dict]:
        """Read data from input file and return raw data"""
        with open(input_path, "r") as json_file:
            raw_data = json.load(json_file)
            if not isinstance(raw_data, list):
                raise ValueError("JSON should be a list type")
            return raw_data

    def write_data(self, output_path: Path, dump: str):
        """Write prepared data in to the file"""
        with open(output_path, "a") as json_file:
            json_file.write(dump)

    def _write_in_batches(self, objects: Generator, output_path: Path, batch_size=5):
        """Writes data with batching aproach"""
        batch: list[str] = []

        for item in objects:
            match item:
                case Car():
                    if not self._is_data_new(item.vin):
                        continue
                    self.processed_vins.add(item.vin)

                    data = item.model_dump()
                    data["content"] = item.ai_description
                    flat_dict = flatten(data)
                    batch.append(json.dumps(flat_dict))

                case _:
                    raise TypeError("Wrong data type")

            if len(batch) >= batch_size:
                self.write_data(output_path, "\n".join(batch) + "\n")
                batch.clear()

        if batch:
            self.write_data(output_path, "\n".join(batch) + "\n")
            batch.clear()

    def _is_data_new(self, vin: str) -> bool:
        """Dublicate filter"""
        if vin not in self.processed_vins:
            return True
        return False

    def data_transform(self, input_path: Path, output_path: Path):
        """Manage data transformation from JSON to JSONL"""
        logging.info(f"Transforming data from [{input_path}] to [{output_path}] ")

        try:
            raw_data = self.read_data(input_path)
            car_generator = (Car.model_validate(item) for item in raw_data)
            self._write_in_batches(objects=car_generator, output_path=output_path)

            logging.info(
                f"{len(self.processed_vins)} objects processed from {input_path}"
            )
        except Exception as e:
            logging.exception(f"Error validation: {e}")
