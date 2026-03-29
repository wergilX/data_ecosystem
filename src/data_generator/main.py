import logging

import click

from .generators.aircraft_generator import AircraftGenerator
from .generators.car_generator import CarGenerator
from .generators.motorcycle_generator import MotorcycleGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@click.command()
@click.option(
    "--type",
    type=click.Choice(["car", "motorcycle", "aircraft"], case_sensitive=True),
    default="car",
    prompt="Vehicle type (car, motorcycle, aircraft)",
    help="The type of vehicle to generate.",
)
@click.option(
    "--count",
    type=click.IntRange(1, 1000),
    default=1,
    prompt="Count of vehicles to generate",
    help="The count of vehicles to generate in JSONs (1-1000).",
)
def generate_vehicles(type, count):
    """CLI tool to generate vehicle data in JSON format."""

    generators = {
        "car": CarGenerator,
        "motorcycle": MotorcycleGenerator,
        "aircraft": AircraftGenerator,
    }

    click.echo(f"Generating {count} {type}(s)...")

    try:
        generator_class = generators[type]
        generator = generator_class()

        vehicles = generator.generate(count)
        generator.to_json(vehicles)

        click.secho("Successfully generated!", fg="green")
    except Exception as e:
        logging.error(f"Failed to generate: {e}")
        click.secho(f"Error: {e}", bold=True, fg="red")


if __name__ == "__main__":
    generate_vehicles()
