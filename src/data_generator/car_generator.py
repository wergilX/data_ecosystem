import json
from pathlib import Path

from faker import Faker
from typing import List

from .car import Car, Engine, Metadata, TechnicalSpecs
from .vehicle import Vehicle
from .vehicle_generator import VehicleGenerator
from datetime import datetime
import logging


class CarGenerator(VehicleGenerator):
    """Generator for car objects with nested metadata and technical specs."""

    base_path: Path = Path("./cars")

    def generate(self) -> Vehicle:
        """Generate car obj with data"""
        fake = Faker()
        car = Car(
            vin=fake.bothify(text="???###???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            brand=fake.random_element(elements=("Tesla", "BMW", "Ford", "Toyota")),
            model=fake.random_element(
                elements=("Model 3", "Model S", "Model X", "Model Y")
            ),
            metadata=Metadata(
                year=fake.random_int(min=2020, max=2024),
                factory=fake.random_element(
                    elements=("Giga Berlin", "Giga Texas", "Giga New York")
                ),
            ),
            technical_specs=TechnicalSpecs(
                engine=Engine(
                    type=fake.random_element(elements=("Electric", "Hybrid")),
                    horsepower=fake.random_int(min=200, max=500),
                )
            ),
            features=[fake.word() for _ in range(fake.random_int(min=1, max=5))],
        )
        return car

    def to_one_json(self, count: int):
        """
        Generate multiple car data in to one json file
        param: count - Count of generated vehicles in to file
        """
        try:
            cars: List[dict] = []

            for _ in range(count):
                car = self.generate().to_dict()
                cars.append(car)

            file_path = Path(f"{str(self.base_path)}/log_cars_{datetime.now()}.json")
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w") as json_file:
                json.dump(cars, json_file, indent=4)

            logging.info(f"Log file generated with {count} cars in {file_path}")
        except Exception as e:
            logging.exception(f"Error writing to JSON file: {e}")
    
    def to_multiple_jsons(self, count: int):
        """
        Generate cars data in to a multiple json files
        param: count - Count of generated cars in to separated files
        """
        try:
            for _ in range(count):
                car = self.generate().to_dict()
                file_path = Path(f"{str(self.base_path)}/log_car_{car.get("vin")}_{datetime.now()}.json")
                file_path.parent.mkdir(parents=True, exist_ok=True)

                with open(file_path, "w") as json_file:
                    json.dump(car, json_file, indent=4)

            logging.info(f"{count} log files generated in {self.base_path}")
        except Exception as e:
            logging.exception(f"Error writing to JSON file: {e}")

    def to_dict(self) -> dict:
        """Generate car data and return as dict"""
        return self.generate().to_dict()
