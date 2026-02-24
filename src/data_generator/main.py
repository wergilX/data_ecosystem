import click

from .car_generator import CarGenerator


@click.command()
@click.option(
    "--count",
    default=1,
    prompt="Count of vehicles to generate",
    type=click.INT,
    help="The count of json files with vehicles.",
)
def main(count: int):
    """Main function to generate vehicle data and write it to a JSON file."""
    car_gen = CarGenerator()

    for _ in range(count):
        car_gen.to_json()

    click.echo("Log file generated")


if __name__ == "__main__":
    main()
