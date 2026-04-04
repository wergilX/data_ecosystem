from typing import List

from pydantic import BaseModel, ConfigDict, Field

from data_ingestor.schemas.base import Vehicle


class Metadata(BaseModel):
    year: int = Field(ge=2020, le=2100)
    factory: str = Field(min_length=1)


class Engine(BaseModel):
    type: str = Field(min_length=1)
    horsepower: int = Field(gt=0)


class TechnicalSpecs(BaseModel):
    engine: Engine


class Car(BaseModel, Vehicle):
    model_config = ConfigDict(extra="forbid")

    type: str = Field(min_length=1)
    vin: str = Field(min_length=1)
    brand: str = Field(min_length=1)
    model: str = Field(min_length=1)
    metadata: Metadata
    technical_specs: TechnicalSpecs
    features: List[str]

    @property
    def ai_description(self) -> str:
        """Represent class data in a pretty readable text"""
        return (
            f"This car is a {self.brand} {self.model} manufactured in {self.metadata.year}. "
            f"It has a {self.technical_specs.engine.type} engine with "
            f"{self.technical_specs.engine.horsepower} horsepower."
            f"This car has a features like: {', '.join(self.features)}."
        )
