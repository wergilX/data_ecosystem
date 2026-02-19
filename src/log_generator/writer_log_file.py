from pathlib import Path


class WriterLogFile:
    """Class that writes log messages to a file."""

    def __init__(self, file_path: str, max_file_size: int):
        self.file_path = Path(file_path)
        self.file_path.touch(exist_ok=True)
        self.max_file_size = max_file_size

    def __enter__(self):
        self._file = self.file_path.open("a")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()

    def write_message(self, message: str) -> bool:
        """Method that writes a log message to a file and returns whether the file size exceeds the maximum."""
        self._file.write(message + "\n")
        self._file.flush()
        # return True if the file size exceeds the maximum, False otherwise
        return self._file.tell() >= self.max_file_size
