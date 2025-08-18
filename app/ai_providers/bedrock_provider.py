import json, logging, boto3

from enum import Enum
from botocore.exceptions import ClientError
from .base_provider import BaseProvider

logger = logging.getLogger(__name__)


class BedrockModels(Enum):
    TITAN_TEXT_EXPRESS = "amazon.titan-text-express-v1",
    CLAUDE_V2 = "anthropic.claude-v2"


class BedrockProvider(BaseProvider):
    def __init__(self,
                 region='us-east-1',
                 model_id: BedrockModels = BedrockModels.TITAN_TEXT_EXPRESS):
        self.brt = boto3.client("bedrock-runtime", region_name=region)
        self.model_id: str = model_id.name

    def generate_response(self, prompt: str) -> str:
        """
        Invokes the specified model with the supplied prompt.
        param prompt: The prompt that you want to send to the model.

        :return: The text response from the model.
        """

        # Format the request payload using the model's native structure.
        native_request = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
                "topP": 0.9
            }
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        try:
            # Invoke the model with the request.
            response = self.brt.invoke_model(modelId=self.model_id, body=request)

            # Decode the response body.
            model_response = json.loads(response["body"].read())

            # Extract and print the response text.
            response_text = model_response["results"][0]["outputText"]
            return response_text

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
            raise
