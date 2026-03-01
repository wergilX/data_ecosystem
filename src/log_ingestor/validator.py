from typing import List

from pydantic import BaseModel, field_validator


class Metadata(BaseModel):
    year: int
    factory: str


class Engine(BaseModel):
    type: str
    horsepower: int


class TechnicalSpecs(BaseModel):
    engine: Engine


class Car(BaseModel):
    vin: str
    brand: str
    model: str
    metadata: Metadata
    technical_specs: TechnicalSpecs
    features: List[str]

    @field_validator("vin")
    def vin_validation(cls, vin):
        if vin != "XY789012345":
            raise TypeError("LOL")
        return vin
