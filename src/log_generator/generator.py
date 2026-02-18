from faker import Faker


class MessageGenerator:
    _log_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    _messages = (
        "User not found",
        "Connection error",
        "Failed to process request",
        "Writing to file failed",
        "Writing to DB failed",
    )

    def __init__(self):
        self.faker = Faker()

    def generate_message(self) -> str:
        timestamp = f"{self.faker.date_time_this_year()}"
        level = f"{self.faker.random_element(elements=self._log_levels)}"
        message = f"{self.faker.random_element(elements=self._messages)}"
        return f"{timestamp} {level} {message}"
