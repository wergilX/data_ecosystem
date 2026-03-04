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

    def generate(self, count: int):
        """Generate car objects with data"""
        self.objects: list[Car] = []
        fake = Faker()
        for _ in range(count):
            car = Car(
                vin=fake.bothify(
                    text="???###???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                ),
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
            self.objects.append(car)
        logging.info(f"{count} cars data generated")

    def to_json(self):
        """
        Generate multiple car data in to one json file
        param: count - Count of generated vehicles in to file
        """
        try:
            file_path = Path(self.base_path / f"log_cars_{datetime.now()}.json")
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w") as json_file:
                json.dump([asdict(item) for item in self.objects], json_file, indent=4)

            logging.info(f"Log file created in {file_path}")
        except Exception as e:
            logging.exception(f"Error writing to JSON file: {e}")
