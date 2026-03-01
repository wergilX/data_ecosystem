import click

from .file_reader import file_transformer


@click.command()
# @click.option("--input", prompt="Input file or folder",  help="Input JSON file or folder with jsons")

# @click.option("--output", prompt="output file path", help="Output path for JSONL file.")
def main():
    """Program that transform JSON files in to JSONL"""
    file_in = "./test.json"
    file_out = "./test.jsonl"

    # print(f"input({file_path})")
    file_transformer(file_in, file_out)


if __name__ == "__main__":
    main()
