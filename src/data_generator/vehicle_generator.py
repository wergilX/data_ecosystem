from abc import ABC, abstractmethod
from pathlib import Path

from .vehicle import Vehicle


class VehicleGenerator(ABC):
    base_path: Path = Path(".")  # Each class must override path for type of vehicle

    @abstractmethod
    def generate(self) -> Vehicle:
        """Generate concrete vehicle with technical specs and features"""
        pass

    @abstractmethod
    def to_json(self):
        """Write vehicle data in to a json"""

    @abstractmethod
    def to_dict(self) -> dict:
        """Write vehicle data in to a json"""
