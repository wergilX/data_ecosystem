from dataclasses import asdict, dataclass
from typing import List

from .vehicle import Vehicle


@dataclass
class Metadata:
    year: int
    factory: str


@dataclass
class Engine:
    type: str
    horsepower: int


@dataclass
class TechnicalSpecs:
    engine: Engine


@dataclass
class Motorcycle(Vehicle):
    type: str
    vin: str
    brand: str
    model: str
    has_sidecar: bool
    metadata: Metadata
    technical_specs: TechnicalSpecs
    features: List[str]

    def to_dict(self) -> dict:
        """Convert the Motorcycle dataclass instance to a dictionary."""
        return asdict(self)
