import json
from pathlib import Path

from .validator import Car


def file_read(file_path: str):
    file = Path(file_path)
    if not file.exists():
        raise ValueError(f"Wrong path {file_path}")
    with open(file, "r") as json_file:
        data: Car = json.load(json_file)
        print(f"{data}")
