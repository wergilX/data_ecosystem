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
    def to_one_json(self, count: int):
        """
        Generate multiple vehicle data in to one json file
        param: count - Count of generated vehicles in to file
        """

    @abstractmethod
    def to_multiple_jsons(self, count: int):
        """
        Generate vehicle data in to a multiple json files
        param: count - Count of generated vehicles in to separated files
        """

    @abstractmethod
    def to_dict(self) -> dict:
        """Transform vehicle data as dict"""