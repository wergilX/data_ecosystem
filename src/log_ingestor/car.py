from typing import List

from pydantic import BaseModel, field_validator


class Metadata(BaseModel):
    year: int
    factory: str

    @field_validator("year")
    @classmethod
    def check_hp(cls, value: int):
        if value < 1900:
            raise ValueError("The car can't be older than 1900")
        return value


class Engine(BaseModel):
    type: str
    horsepower: int

    @field_validator("horsepower")
    @classmethod
    def check_hp(cls, value: int):
        if value <= 0:
            raise ValueError("The car can't be with 0 horsepower")
        return value


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
    @classmethod
    def check_hp(cls, value: str):
        return value.upper()
