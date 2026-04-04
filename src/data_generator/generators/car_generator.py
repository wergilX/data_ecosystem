import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from faker import Faker

from ..dataclasses.car import Car, Engine, Metadata, TechnicalSpecs
from ..dataclasses.vehicle import Vehicle
from .vehicle_generator import VehicleGenerator


class CarGenerator(VehicleGenerator):
    """Generator for car objects with nested metadata and technical specs."""

    base_path: Path = Path("./cars")

    def __init__(self):
        self.faker = Faker()

    def _create_car(self) -> Car:
        """Generate single car object with data"""
        return Car(
            type="car",
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

    def generate(self, count: int) -> list[Vehicle]:
        """Generate multiple car objects with data."""
        logging.info(f"{count} cars data generated.")
        cars: list[Vehicle] = [self._create_car() for _ in range(count)]
        return cars

    def to_json(self, vehicles, path=None):
        """Generate JSONs with car data."""
        if path is None:
            path = self.base_path

        try:
            for vehicle in vehicles:
                file_path = path / f"car_{vehicle.vin}_{datetime.now().date()}.json"
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w") as json_file:
                    json.dump(asdict(vehicle), json_file, indent=4)

            logging.info(
                f"Files were successfully created in the folder: '{path.absolute()}'"
            )
        except Exception as e:
            logging.exception(f"Error writing to JSON file: {e}")
