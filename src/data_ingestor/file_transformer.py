import json
import logging
from pathlib import Path
from typing import Generator

from .car import Car


class FileTransformer:
    def __init__(self):
        """Create container with processed vin"""
        self.processed_vins = set()

    def read_data(self) -> list[dict]:
        """Read data from input file and return raw data"""
        with open(self.input_path, "r") as json_file:
            raw_data = json.load(json_file)
            if not isinstance(raw_data, list):
                raise ValueError("JSON should have list type")
            return raw_data

    def write_data(self, dump: str):
        """Write prepared data in to the file"""
        with open(self.output_path, "a") as json_file:
            json_file.write(dump)

    def write_in_batches(self, generator: Generator[Car], batch_size=5):
        """Writes data with batching aproach"""
        batch: list[str] = []

        for car in generator:
            if not self.is_data_new(car.vin):
                continue

            data = car.model_dump()
            data["content"] = car.ai_description

            batch.append(json.dumps(data))

            if len(batch) >= batch_size:
                self.write_data("\n".join(batch) + "\n")
                batch.clear()

        if batch:
            self.write_data("\n".join(batch) + "\n")
            batch.clear()

    def is_data_new(self, vin: str) -> bool:
        """Dublicate filter"""
        if vin not in self.processed_vins:
            self.processed_vins.add(vin)
            return True
        return False

    def data_transform(self, input: Path, output: Path):
        """Manage data transformation from JSON to JSONL"""
        logging.info(f"Importing data from [{input}] to [{output}] ")

        self.input_path = input
        self.output_path = output
        try:
            raw_data = self.read_data()
            car_gen = (Car.model_validate(item) for item in raw_data)
            self.write_in_batches(car_gen)

            logging.info(f"{self.processed_vins} objects processed from {input}")
        except Exception as e:
            logging.exception(f"Error validation: {e}")
