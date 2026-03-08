import logging
from pathlib import Path

import click

from .file_transformer import FileTransformer

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
    prompt="output file with path './example.jsonl'",
    help="Output file with path for JSONL file.",
)
def main(input, output):
    """Script that transforms JSON files into JSONL"""
    # Check input folder
    path = Path(input)
    if not path.exists():
        raise ValueError(f"Wrong file {input}")

    # Create output file if it's not exist
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Processing data
    file_transformer = FileTransformer()
    if path.is_file():
        file_transformer.data_transform(path, out_path)
    else:
        json_files = (f for f in path.rglob("*.json") if f.is_file())
        for item in json_files:
            file_transformer.data_transform(item, out_path)


if __name__ == "__main__":
    main()
