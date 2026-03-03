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
    type=click.INT,
    default=1,
    prompt="Count of vehicles to generate",
    help="The count of vehicles to generate in JSON.",
)
def main(count: int):
    """Main function to generate vehicle data and write it to a JSON file."""
    car_gen = CarGenerator()
    car_gen.to_one_json(count)


if __name__ == "__main__":
    main()
