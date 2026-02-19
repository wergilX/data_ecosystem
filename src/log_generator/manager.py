class Manager:
    """Class that manages the log generation process."""

    def __init__(self, generator, writer):
        self.generator = generator
        self.writer = writer

    def generate_logs(self):
        """Method that manages the log generation process."""
        with self.writer as writer:
            while True:
                message = self.generator.generate_message()
                if writer.write_message(message):
                    break
