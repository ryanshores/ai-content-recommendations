from abc import ABC, abstractmethod

class BaseClient(ABC):
    @abstractmethod
    def get_movie_recommendations(self, input: str) -> str:
        """
        Abstract method to get movie recommendations based on user input.

        :param input: A string containing the user input.
        :return: A string containing movie recommendations.
        """
        pass