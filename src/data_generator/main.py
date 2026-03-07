import logging

import click

from .car_generator import CarGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@click.command()
@click.option(
    "--count",
    type=click.IntRange(1, 1000),
    default=1,
    prompt="Count of vehicles to generate",
    help="The count of vehicles to generate in JSON (1-1000).",
)
def main(count: int):
    """Main function to generate vehicle data and write it to a JSON file."""
    car_gen = CarGenerator()
    car_gen.generate(count)
    car_gen.to_json()


if __name__ == "__main__":
    main()
