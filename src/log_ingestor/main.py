import click
from .file_reader import file_read


@click.command()
#@click.option("--input", prompt="Input file or folder",  help="Input JSON file or folder with jsons")

#@click.option("--output", prompt="output file path", help="Output path for JSONL file.")
def main():
    """Program that transform JSON files in to JSONL"""
    file_path = "./test.json"
    print(f"input({file_path})")
    file_read(file_path)

    

if __name__ == "__main__":
    main()
