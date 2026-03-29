import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from faker import Faker

from ..dataclasses.motorcycle import Engine, Metadata, Motorcycle, TechnicalSpecs
from ..dataclasses.vehicle import Vehicle
from .vehicle_generator import VehicleGenerator


class MotorcycleGenerator(VehicleGenerator):
    """Generator for motorcycle objects with nested metadata and technical specs."""

    base_path: Path = Path("./motorcycles")

    def __init__(self):
        self.faker = Faker()

    def _create_motorcycle(self) -> Motorcycle:
        """Generate single motorcycle object with data."""
        return Motorcycle(
            type="motorcycle",
            vin=self.faker.bothify(
                text="MOT###???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ),
            brand=self.faker.random_element(
                elements=(
                    "Ducati",
                    "Harley-Davidson",
                    "Yamaha",
                    "Kawasaki",
                    "BMW Motorrad",
                )
            ),
            model=self.faker.random_element(
                elements=("Ninja", "Monster", "Iron 883", "R 1250 GS", "MT-07")
            ),
            has_sidecar=self.faker.boolean(chance_of_getting_true=10),
            metadata=Metadata(
                year=self.faker.random_int(min=2015, max=2024),
                factory=self.faker.random_element(
                    elements=("Bologna Plant", "Milwaukee Factory", "Iwata Plant")
                ),
            ),
            technical_specs=TechnicalSpecs(
                engine=Engine(
                    type=self.faker.random_element(
                        elements=("V-Twin", "Inline-4", "Boxer")
                    ),
                    horsepower=self.faker.random_int(min=50, max=210),
                )
            ),
            features=[
                self.faker.word() for _ in range(self.faker.random_int(min=1, max=3))
            ],
        )

    def generate(self, count: int) -> list[Vehicle]:
        """Generate multiple motorcycle objects with data."""
        logging.info(f"{count} motorcycles data generated.")
        motorcycles: list[Vehicle] = [self._create_motorcycle() for _ in range(count)]
        return motorcycles

    def to_json(self, vehicles, path=None):
        """Generate JSONs with motorcycle data."""
        if path is None:
            path = self.base_path

        try:
            for vehicle in vehicles:
                file_path = path / f"moto_{vehicle.vin}_{datetime.now().date()}.json"
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w") as json_file:
                    json.dump(asdict(vehicle), json_file, indent=4)

            logging.info(f"Log files created in folder: '{path.absolute()}'")
        except Exception as e:
            logging.exception(f"Error writing to JSON file: {e}")
