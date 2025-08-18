import subprocess

from app.clients.base_client import BaseClient


class OllamaClient(BaseClient):
    def __init__(self, model="llama2"):
        self.model = model
        self.timeout = 15

    def _run_command(self, prompt: str) -> str:
        """
        Runs a command using the Ollama CLI to generate text based on the provided prompt.
        :param prompt: The prompt to send to the model.
        :return: The generated text response from the model.
        """
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                check=True,
                timeout=self.timeout,
                stdin=subprocess.DEVNULL  # important
            )
            print(result.stdout)
            # Ollama CLI prints to stdout
            output = result.stdout.strip()
            if not output:
                return "Ollama returned empty output."
            return output
        except subprocess.TimeoutExpired:
            return f"Error: Ollama run timed out after {self.timeout} seconds."
        except subprocess.CalledProcessError as e:
            return f"Error: Ollama run failed: {e.stderr.strip()}"
        except FileNotFoundError:
            return "Error: Ollama CLI not found. Make sure it is installed and in your PATH."
        except Exception as e:
            return f"Unexpected error: {e}"

    def get_movie_recommendations(self, user_input: str) -> str:
        prompt = f"Recommend 3 movies based on this request: {user_input}."

        # Use Ollama CLI to generate text
        return self._run_command(prompt)