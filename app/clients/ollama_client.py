import subprocess

from app.clients.base_client import BaseClient


class OllamaClient(BaseClient):
    def __init__(self, model="llama2"):
        self.model = model

    def _run_command(self, prompt: str) -> str:
        """
        Runs a command using the Ollama CLI to generate text based on the provided prompt.
        :param prompt: The prompt to send to the model.
        :return: The generated text response from the model.
        """
        result = subprocess.run(
            ["ollama", "run", self.model, prompt],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        return result.stdout.strip()

    def get_movie_recommendations(self, user_input: str) -> str:
        prompt = f"Recommend 3 movies based on this request: {user_input}"

        # Use Ollama CLI to generate text
        return self._run_command(prompt)