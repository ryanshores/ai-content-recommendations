import os

ENV = os.getenv("APP_ENV", "local")
PROVIDER_TYPE = os.getenv("PROVIDER", "ollama")  # options: 'hf', 'bedrock', 'ollama'

if PROVIDER_TYPE == "bedrock":
    from app.ai_providers.bedrock_provider import BedrockProvider
    provider = BedrockProvider()
elif PROVIDER_TYPE == "ollama":
    from app.ai_providers.ollama_provider import OllamaProvider
    provider = OllamaProvider(model="llama2")
else:
    from app.ai_providers.hugging_face_provider import HuggingFaceProvider
    provider = HuggingFaceProvider(model="distilgpt2")