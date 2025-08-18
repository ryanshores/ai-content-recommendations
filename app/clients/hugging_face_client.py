from .base_client import BaseClient
from transformers import pipeline


class HuggingFaceClient(BaseClient):
    def __init__(self, model="gpt2"):
        # You can swap in any local model, like "distilgpt2" or "tiiuae/falcon-7b-instruct"
        self.generator = pipeline("text-generation", model=model)

    def get_movie_recommendations(self, user_input: str) -> str:
        prompt = f"Recommend 3 movies based on this request: {user_input}"
        outputs = self.generator(prompt, max_length=80, num_return_sequences=1)
        return outputs[0]["generated_text"]