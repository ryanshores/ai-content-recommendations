import os

ENV = os.getenv("APP_ENV", "local")
PROVIDER_TYPE = os.getenv("PROVIDER", "ollama")  # options: 'hf', 'bedrock', 'ollama'

if PROVIDER_TYPE == "bedrock":
    from app.clients.bedrock_client import BedrockClient
    client = BedrockClient()
elif PROVIDER_TYPE == "ollama":
    from app.clients.ollama_client import OllamaClient
    client = OllamaClient(model="llama2")
else:
    from app.clients.hugging_face_client import HuggingFaceClient
    client = HuggingFaceClient(model="distilgpt2")