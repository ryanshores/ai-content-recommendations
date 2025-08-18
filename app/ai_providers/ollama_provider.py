import subprocess, logging, requests

from .base_provider import BaseProvider

logger = logging.getLogger(__name__)


class OllamaProvider(BaseProvider):
    host = "http://localhost:11434"

    def __init__(self, model="llama2"):
        self.model = model
        self.timeout = 15
        self._start_server()

    def _start_server(self):
        try:
            status = requests.get(self.host)

            if status.status_code != 200:
                logger.info("Starting Ollama server...")
                subprocess.run(["ollama", "serve", self.model])

        except Exception as e:
            logger.error("Error starting Ollama server.")

    def _run_request(self, prompt: str) -> str:
        """
        Runs a request to the Ollama server to generate text based on the provided prompt.
        :param prompt: The prompt to send to the model.
        :return: The generated text response from the model.
        """
        self._start_server()

        try:
            resp = requests.post(f"{self.host}/api/generate", json={"model": self.model, "prompt": prompt})
            return resp.json().get("completion", "No response")
        except Exception as e:
            return f"Error: {e}"

    def _run_request_with_streaming(self, prompt: str):
        """
        Runs a request to the Ollama server to generate text based on the provided prompt with streaming.
        :param prompt: The prompt to send to the model.
        :return: A generator yielding the generated text response from the model.
        """
        self._start_server()

        try:
            with requests.post(f"{self.host}/api/generate", json={"model": self.model, "prompt": prompt}, stream=True) as resp:
                for line in resp.iter_lines():
                    if line:
                        # Each line is JSON
                        try:
                            data = line.decode("utf-8")
                            yield f"data: {data}\n\n"  # SSE format
                        except Exception:
                            continue
        except Exception as e:
            yield f"Error: {e}"

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

    def generate_response(self, prompt: str) -> str:
        return self._run_command(prompt)