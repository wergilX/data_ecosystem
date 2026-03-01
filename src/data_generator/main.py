import click

from .car_generator import CarGenerator


@click.command()
@click.option(
    "--count",
    type=click.INT,
    default=1,
    prompt="Count of vehicles to generate",
    help="The count of vehicles to generate in JSON.",
)
def main(split: bool, count: int):
    """Main function to generate vehicle data and write it to a JSON file."""
    car_gen = CarGenerator()
    car_gen.to_one_json(count)

    click.echo("Log file generated")


if __name__ == "__main__":
    main()
