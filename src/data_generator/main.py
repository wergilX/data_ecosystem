import click

from .car_generator import CarGenerator


@click.command()
@click.option(
    "--split",
    type=click.BOOL,
    default=True,
    prompt="Generate all vehicles in one file or individualy?",
    help="Option to generate all vehicles in one file or individualy"

)
@click.option(
    "--count",
    type=click.INT,
    default=1,
    prompt="Count of vehicles to generate",
    help="The count of json files with vehicles.",
)
def main(split: bool, count: int):
    """Main function to generate vehicle data and write it to a JSON file."""
    car_gen = CarGenerator()

    if split:
        car_gen.to_multiple_jsons(count)
    else:
        car_gen.to_one_json(count)

    click.echo("Log files generated")


if __name__ == "__main__":
    main()
