import json
from pathlib import Path

from faker import Faker

from .car import Car, Engine, Metadata, TechnicalSpecs
from .vehicle import Vehicle
from .vehicle_generator import VehicleGenerator


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

    def to_json(self):
        """Generate car data in to a json"""
        try:
            car = self.generate().to_dict()
            file_path = Path(f"{str(self.base_path)}/{car.get('vin')}.json")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            print(self.base_path)
            print(file_path)

            with open(file_path, "w") as json_file:
                json.dump(car, json_file, indent=4)

        except Exception as e:
            print(f"Error writing to JSON file: {e}")

    def to_dict(self) -> dict:
        """Generate car data as dict"""
        return self.generate().to_dict()
