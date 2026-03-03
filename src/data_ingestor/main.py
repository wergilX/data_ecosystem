from pathlib import Path

import click

from .file_transformer import FileTransformer


@click.command()
@click.option(
    "--input",
    prompt="Input file or folder",
    help="Input JSON file or folder with jsons",
)
@click.option(
    "--output",
    prompt="output file with path './example.json'",
    help="Output file with path for JSONL file.",
)
def main(input, output):
    """Program that transform JSON files in to JSONL"""
    path = Path(input)
    if not path.exists():
        raise ValueError(f"Wrong file {input}")

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    file_transformer = FileTransformer()
    if path.is_file():
        file_transformer.data_transform(path, out_path)
    else:
        json_files = (f for f in path.rglob("*.json") if f.is_file())
        for item in json_files:
            file_transformer.data_transform(item, out_path)


if __name__ == "__main__":
    main()
