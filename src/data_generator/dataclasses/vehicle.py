from abc import ABC, abstractmethod


class Vehicle(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the dataclass instance to a dictionary."""
        pass
