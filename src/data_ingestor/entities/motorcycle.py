from typing import List

from pydantic import BaseModel, ConfigDict, field_validator

from ..exceptions import HorspowerError, VinError, YearError


class Metadata(BaseModel):
    year: int
    factory: str

    @field_validator("year")
    @classmethod
    def check_year(cls, value: int):
        if value <= 0:
            raise YearError("Year can't be negative")
        return value


class Engine(BaseModel):
    type: str
    horsepower: int

    @field_validator("horsepower")
    @classmethod
    def check_hp(cls, value: int):
        if value < 0:
            raise HorspowerError("The motorcycle can't be with negative horsepower")
        return value


class TechnicalSpecs(BaseModel):
    engine: Engine


class Motorcycle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str
    vin: str
    brand: str
    model: str
    has_sidecar: bool
    metadata: Metadata
    technical_specs: TechnicalSpecs
    features: List[str]

    @field_validator("vin")
    @classmethod
    def check_vin(cls, value: str):
        if not value:
            raise VinError("VIN must be provided")
        return value

    @property
    def ai_description(self) -> str:
        """Represent class data in a pretty readable text"""
        return (
            f"This motorcycle is a {self.brand} {self.model} manufactured in {self.metadata.year}. "
            f"It has a {self.technical_specs.engine.type} engine with "
            f"{self.technical_specs.engine.horsepower} horsepower."
            f"This motorcycle has a features like: {', '.join(self.features)}."
        )
