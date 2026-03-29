import json
import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from faker import Faker

from ..dataclasses.aircraft import Aircraft, Engine, Metadata, TechnicalSpecs
from ..dataclasses.vehicle import Vehicle
from .vehicle_generator import VehicleGenerator


class AircraftGenerator(VehicleGenerator):
    """Generator for aircraft objects with nested metadata and flight specs."""

    base_path: Path = Path("./aircrafts")

    def __init__(self):
        self.faker = Faker()

    def _create_aircraft(self) -> Aircraft:
        """Generate single aircraft object with data"""
        return Aircraft(
            type="aircraft",
            vin=self.faker.bothify(
                text="AIR-####-???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ),
            brand=self.faker.random_element(
                elements=("Boeing", "Airbus", "Cessna", "Embraer", "Bombardier")
            ),
            model=self.faker.random_element(
                elements=("737 Max", "A320neo", "172 Skyhawk", "E195", "Global 7500")
            ),
            metadata=Metadata(
                year=self.faker.random_int(min=1990, max=2024),
                factory=self.faker.random_element(
                    elements=("Everett Factory", "Toulouse Plant", "Wichita Facility")
                ),
            ),
            technical_specs=TechnicalSpecs(
                engine=Engine(
                    type=self.faker.random_element(
                        elements=("Turbofan", "Turboprop", "Piston")
                    ),
                    horsepower=self.faker.random_int(min=150, max=25000),
                ),
                max_altitude=self.faker.random_int(min=10000, max=45000),
            ),
            features=[
                self.faker.word() for _ in range(self.faker.random_int(min=2, max=6))
            ],
        )

    def generate(self, count: int) -> list[Vehicle]:
        """Generate multiple aircraft objects with data"""
        logging.info(f"{count} aircrafts data generated")
        aircrafts: list[Vehicle] = [self._create_aircraft() for _ in range(count)]
        return aircrafts

    def to_json(self, vehicles, path=None):
        """Generate JSONs with aircraft data."""
        if path is None:
            path = self.base_path

        try:
            for vehicle in vehicles:
                file_path = (
                    path / f"aircraft_{vehicle.vin}_{datetime.now().date()}.json"
                )

                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, "w") as json_file:
                    json.dump(asdict(vehicle), json_file, indent=4, ensure_ascii=False)

            logging.info(f"Log files created in folder: '{path.absolute()}'")
        except Exception as e:
            logging.exception(f"Error writing to JSON file: {e}")
