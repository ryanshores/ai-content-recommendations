import subprocess, logging, requests
from abc import ABC
from typing import Generator, Dict, Any

from .base_provider import BaseProvider

logger = logging.getLogger(__name__)


def _process_streaming_response(response: requests.Response) -> Generator[str, None, None]:
    """Process the streaming response and format it as SSE data."""
    for line in response.iter_lines():
        if not line:
            continue

        try:
            data = line.decode("utf-8")
            yield f"data: {data}\n\n"
        except UnicodeDecodeError:
            continue


class OllamaProvider(BaseProvider, ABC):
    OLLAMA_HOST = "http://localhost:11434"
    API_GENERATE_ENDPOINT = "/api/generate"


    def __init__(self, model="llama2"):
        self.model = model
        self.timeout = 15
        self._start_server()

    def _start_server(self):
        try:
            status = requests.get(self.OLLAMA_HOST)

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
            json = {"model": self.model, "prompt": prompt, "stream": False}
            resp = requests.post(f"{self.OLLAMA_HOST}/api/generate", json=json)
            return resp.json().get("response", "No response")
        except Exception as e:
            return f"Error: {e}"


    def _run_request_with_streaming(self, prompt: str) -> Generator[str, None, None]:
        """
        Runs a request to the Ollama server to generate text based on the provided prompt with streaming.
        :param prompt: The prompt to send to the model.
        :return: SSE formatted response strings from the model.
        """
        self._start_server()

        request_payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        try:
            with requests.post(f"{self.OLLAMA_HOST}{self.API_GENERATE_ENDPOINT}",
                               json=request_payload) as response:
                yield from _process_streaming_response(response)
        except requests.RequestException as e:
            yield f"data: {{'error': '{str(e)}'}}\n\n"


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
        return self._run_request(prompt)

    def generate_response_stream(self, prompt: str) -> Generator[str, None, None]:
        yield from self._run_request_with_streaming(prompt)