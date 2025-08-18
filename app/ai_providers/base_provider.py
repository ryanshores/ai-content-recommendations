from abc import ABC, abstractmethod

class BaseProvider(ABC):

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Abstract method to get ai response from prompt.

        :param prompt: A string containing the prompt.
        :return: A string containing the response.
        """
        pass