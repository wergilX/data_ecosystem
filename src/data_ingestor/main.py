import logging

import click

from .reader import read_files
from .vehicle_processor import VehicleProcessor
from .writer import BatchWriter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@click.command()
@click.option(
    "--input",
    prompt="Input file or folder",
    help="Input JSON file or folder with jsons",
)
@click.option(
    "--output",
    default="./default.jsonl",
    prompt="Output file with path",
    help="Output file with path for JSONL file.",
)
def main(input, output):
    """Script that transforms JSON files into JSONL"""

    gen_dict = read_files(input)
    batch_writer = BatchWriter(output)
    vehicle_processor = VehicleProcessor()

    # Processing data
    with batch_writer as writer:
        for item in gen_dict:
            data = vehicle_processor.process(item)
            writer.write_in_batches(data)


if __name__ == "__main__":
    main()
