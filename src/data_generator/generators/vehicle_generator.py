from abc import ABC, abstractmethod
from pathlib import Path

from data_generator.dataclasses.vehicle import Vehicle


class VehicleGenerator(ABC):
    base_path: Path = Path(".")  # Each class must override path for type of vehicle

    @abstractmethod
    def generate(self, count: int) -> list[Vehicle]:
        """Generate concrete vehicles with technical specs and features."""
        pass

    @abstractmethod
    def to_json(self, vehicles, path=None):
        """Generating multiple jsons with separate vehicles."""
