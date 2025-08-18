from .base_provider import BaseProvider
from transformers import pipeline


class HuggingFaceProvider(BaseProvider):
    def __init__(self, model="gpt2"):
        # You can swap in any local model, like "distilgpt2" or "tiiuae/falcon-7b-instruct"
        self.generator = pipeline("text-generation", model=model)

    def generate_response(self, prompt: str) -> str:
        outputs = self.generator(prompt, max_length=80, num_return_sequences=1)
        return outputs[0]["generated_text"]

