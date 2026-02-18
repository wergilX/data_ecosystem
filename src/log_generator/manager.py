from pathlib import Path

from generator import MessageGenerator


class Manager:
    """Class that manages the log generation process."""

    def __init__(self, path: str):
        self.path = path
        self.generator = MessageGenerator()

    def generate_logfile(self):
        """Method that runs the log generation process."""
        self.path_validation()
        self.write_logs(1024 * 1024)  # 1 MB
        # self.write_logs(10 * 1024 * 1024)  # 10 MB

    def path_validation(self):
        """Method that validates the path to the log file."""
        if not self.path.endswith(".log"):
            self.path += "default.log"
            print(f"Path is not valid. Using default path: {self.path}")

        Path(self.path).touch(exist_ok=True)

    def write_logs(self, size: int):
        """Method that creates log file with the specified size."""
        with Path(self.path).open("a") as file:
            file_size = 0
            while file_size < size:
                message = self.generator.generate_message()
                file.write(message + "\n")
                file_size = Path(self.path).stat().st_size

            print(f"Log file created with size {file_size} bytes at path {self.path}")
