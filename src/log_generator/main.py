from datetime import datetime
from pathlib import Path

import click
import generators.factory as factory
from manager import Manager
from writer_log_file import WriterLogFile


def create_file_name_with_path(base_dir: str, format_ext: str) -> str:
    timestamp = datetime.now().time().isoformat()
    filename = f"log_{timestamp}.{format_ext}"
    return str(Path(base_dir) / filename)


@click.command()
@click.option(
    "--path",
    default=None,
    prompt="Path to create log file",
    type=click.STRING,
    help="The path to create log file.",
)
@click.option(
    "--format",
    default=None,
    prompt="File format",
    type=click.Choice(["log", "txt"], case_sensitive=False),
    help="The format of the log file.",
)
@click.option(
    "--file-size",
    default=1024 * 1024,  # 1MB
    prompt="File size in bytes",
    type=click.INT,
    help="The size of the log file in bytes.",
)
def main(path: str, format: str, file_size: int):
    generator = factory.get_generator(format)
    file_path = create_file_name_with_path(path, format)
    writer = WriterLogFile(file_path, file_size)
    manager = Manager(generator, writer)
    manager.generate_logs()
    click.echo(f"Log file generated at: {file_path}")


if __name__ == "__main__":
    main()
