from typing import Any, Protocol


class Vehicle(Protocol):
    type: str
    vin: str

    @property
    def ai_description(self) -> str: ...

    def model_dump(self) -> dict[str, Any]: ...
