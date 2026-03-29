import json
import logging

from flatten_json import flatten  # type: ignore[import-untyped]

from .entities.aircraft import Aircraft
from .entities.car import Car
from .entities.motorcycle import Motorcycle
from .entities.protocol import Vehicle


class VehicleProcessor:
    def __init__(self):
        self.processed_vins: set = set()

    def process(self, raw_dict: dict) -> str | None:
        """Process raw data to prepeared JSONL object"""
        logging.info("Process raw data to prepeared JSONL object")
        try:
            # Validate vehicle data with Typing
            validated_vehicle: Vehicle = self._validate_vehicle(raw_dict)

            # Deduplication
            if validated_vehicle.vin in self.processed_vins:
                logging.warning(
                    f"Processed vin was skipped it is duplicate [{validated_vehicle.vin}]"
                )
                return None
            self.processed_vins.add(validated_vehicle.vin)

            # Adding AI description
            data = validated_vehicle.model_dump()
            data["content"] = validated_vehicle.ai_description

            # Flattening
            dump = self.to_flat_str(data)

            return dump
        except Exception as e:
            logging.exception(f"Error processing: {e}")
            raise

    def _validate_vehicle(self, raw_dict: dict) -> Vehicle:
        """Validate dataclasses wit Pydantic"""
        try:
            match raw_dict["type"]:
                case "car":
                    return Car.model_validate(raw_dict)
                case "motorcycle":
                    return Motorcycle.model_validate(raw_dict)
                case "aircraft":
                    return Aircraft.model_validate(raw_dict)
                case _:
                    raise TypeError(
                        f"Current file contain data with unsupported type [{raw_dict['type']}]"
                    )
        except Exception as e:
            logging.exception(f"Error validation: {e}")
            raise

    def to_flat_str(self, nested_dict: dict) -> str:
        """Convert nested dict to the flattened one level dict and return jsonl ready str"""
        flat_dict = flatten(nested_dict)
        return json.dumps(flat_dict)
