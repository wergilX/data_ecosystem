import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from faker import Faker

from .car import Car, Engine, Metadata, TechnicalSpecs
from .vehicle_generator import VehicleGenerator


class CarGenerator(VehicleGenerator):
    """Generator for car objects with nested metadata and technical specs."""

    base_path: Path = Path("./cars")

    def __init__(self):
        self.faker = Faker()
        self.objects: list[Car] = []

    def _create_car(self) -> Car:
        """Generate single car object with data"""
        return Car(
            vin=self.faker.bothify(
                text="???###???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ),
            brand=self.faker.random_element(
                elements=("Tesla", "BMW", "Ford", "Toyota")
            ),
            model=self.faker.random_element(
                elements=("Model 3", "Model S", "Model X", "Model Y")
            ),
            metadata=Metadata(
                year=self.faker.random_int(min=2020, max=2024),
                factory=self.faker.random_element(
                    elements=("Giga Berlin", "Giga Texas", "Giga New York")
                ),
            ),
            technical_specs=TechnicalSpecs(
                engine=Engine(
                    type=self.faker.random_element(elements=("Electric", "Hybrid")),
                    horsepower=self.faker.random_int(min=200, max=500),
                )
            ),
            features=[
                self.faker.word() for _ in range(self.faker.random_int(min=1, max=5))
            ],
        )

    def generate(self, count: int):
        """Generate car objects with data"""
        self.objects = [self._create_car() for _ in range(count)]
        logging.info(f"{count} cars data generated")

    def to_json(self):
        """
        Generate multiple car data in to json file
        """
        try:
            file_path = Path(self.base_path / f"log_cars_{datetime.now()}.json")
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w") as json_file:
                json.dump([asdict(item) for item in self.objects], json_file, indent=4)

            logging.info(f"Log file created in {file_path}")
        except Exception as e:
            logging.exception(f"Error writing to JSON file: {e}")
