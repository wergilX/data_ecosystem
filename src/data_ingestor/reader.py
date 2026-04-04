import json
from collections.abc import Generator
from pathlib import Path


def read_files(input: str) -> Generator[dict, None, None]:
    """This function search all json files from complex path structure and return generator."""
    # Check input folder
    path = Path(input)
    if not path.exists():
        raise ValueError(f"Wrong file {input}")

    # processing JSONs
    if path.is_file():
        yield read_file(path)
    else:
        json_files = (f for f in path.rglob("*.json") if f.is_file())
        if not json_files:
            raise ValueError("Folder is empty")
        for item in json_files:
            yield read_file(item)


def read_file(input_path: Path) -> dict:
    """Read data from input file and return dict"""
    with open(input_path, "r") as json_file:
        raw_data = json.load(json_file)
        if not isinstance(raw_data, dict):
            raise ValueError("JSON should be a dict type")
        return raw_data
