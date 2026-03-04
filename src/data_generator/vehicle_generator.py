from abc import ABC, abstractmethod
from pathlib import Path


class VehicleGenerator(ABC):
    base_path: Path = Path(".")  # Each class must override path for type of vehicle

    @abstractmethod
    def generate(self, count: int):
        """Generate concrete vehicle with technical specs and features"""
        pass

    @abstractmethod
    def to_json(self):
        """
        Generate multiple vehicle data in to one json file
        param: count - Count of generated vehicles in to file
        """
