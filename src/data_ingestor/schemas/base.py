from abc import ABC, abstractmethod
from typing import Any


class Vehicle(ABC):
    type: str
    vin: str

    @property
    @abstractmethod
    def ai_description(self) -> str:
        pass

    @abstractmethod
    def model_dump(self) -> dict[str, Any]:
        pass
