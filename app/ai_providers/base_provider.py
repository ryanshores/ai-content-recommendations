from abc import ABC, abstractmethod
from typing import Generator


class BaseProvider(ABC):

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Abstract method to get ai response from prompt.

        :param prompt: A string containing the prompt.
        :return: A string containing the response.
        """
        pass

    @abstractmethod
    def generate_response_stream(self, prompt: str) -> Generator[str, None, None]:
        """
        Abstract method to get ai response from prompt with streaming.

        :param prompt: A string containing the prompt.
        :return: A generator yielding strings containing the response.
        """
        pass