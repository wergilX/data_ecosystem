from generators.generator_log import GeneratorLog
from generators.generator_txt import GeneratorTxt


def get_generator(generator_type: str):
    generators = {"log": GeneratorLog, "txt": GeneratorTxt}

    generator_class = generators.get(generator_type.lower())
    if generator_class is None:
        raise ValueError(f"Unknown generator type: {generator_type}")
    return generator_class()
