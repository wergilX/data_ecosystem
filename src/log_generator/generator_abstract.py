from abc import ABC, abstractmethod


class GeneratorAbstract(ABC):
    """Abstract class that defines the interface for log generators."""

    @abstractmethod
    def generate_message(self) -> str:
        """Method that generates a log message."""
        pass
