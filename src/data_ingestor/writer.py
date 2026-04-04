from pathlib import Path


class BatchWriter:
    """Accomulate data for write it in batches to reduce file writing operations."""

    def __init__(self, output_path: str, batch_size: int = 5):
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        self.vehicles_batch: list[str] = []
        self.batch_size: int = batch_size
        self.output_path: Path = Path(output_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._flush_batch()

    def write_in_batches(self, dump: str):
        """Writes data with batching approach"""
        if dump is not None:
            self.vehicles_batch.append(dump)
            if len(self.vehicles_batch) >= self.batch_size:
                self._flush_batch()

    def _flush_batch(self):
        """Flush the current batch to file"""
        if self.vehicles_batch:
            self.write_data("\n".join(self.vehicles_batch) + "\n")
            self.vehicles_batch.clear()

    def write_data(self, dump: str):
        """Write prepared data in to the file"""
        with open(self.output_path, "a") as json_file:
            json_file.write(dump)
