import generators.data as data
from faker import Faker
from generators.generator_abstract import GeneratorAbstract


class GeneratorTxt(GeneratorAbstract):
    """Class that generates log messages in txt format."""

    def __init__(self):
        self.faker = Faker()

    def generate_message(self) -> str:
        timestamp = f"{self.faker.date_time_this_year()}"
        level = f"{self.faker.random_element(elements=data.LOG_LEVELS)}"
        message = f"{self.faker.random_element(elements=data.LOG_MESSAGES)}"
        return f"{timestamp} {level} {message}"
