import click
from manager import Manager


@click.command()
@click.option(
    "--path",
    default=None,
    prompt="Path to log file",
    type=click.STRING,
    help="The path to the log file.",
)
def run(path: str):
    """Function that asks the user for a path to the log file and run the log generation process."""
    if not path.endswith(".log"):
        path += "default.log"

    manager = Manager(path)
    manager.generate_logfile()
