from dataclasses import asdict, dataclass
from typing import List

from .vehicle import Vehicle


@dataclass
class Engine:
    type: str
    horsepower: int


@dataclass
class TechnicalSpecs:
    engine: Engine


@dataclass
class Metadata:
    year: int
    factory: str


@dataclass
class Car(Vehicle):
    type: str
    vin: str
    brand: str
    model: str
    metadata: Metadata
    technical_specs: TechnicalSpecs
    features: List[str]

    def to_dict(self) -> dict:
        """Convert the Car dataclass instance to a dictionary."""
        return asdict(self)
