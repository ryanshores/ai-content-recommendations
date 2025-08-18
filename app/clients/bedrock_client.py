import json, logging, boto3
from enum import Enum
from botocore.exceptions import ClientError

from app.clients.base_client import BaseClient

logger = logging.getLogger(__name__)


class BedrockModels(Enum):
    TITAN_TEXT_EXPRESS = "amazon.titan-text-express-v1",
    CLAUDE_V2 = "anthropic.claude-v2"


class BedrockClient(BaseClient):
    def __init__(self,
                 region='us-east-1',
                 model_id: BedrockModels = BedrockModels.TITAN_TEXT_EXPRESS):
        self.brt = boto3.client("bedrock-runtime", region_name=region)
        self.model_id: str = model_id.name

    def _invoke_model(self, prompt):
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

    def get_movie_recommendations(self, input: str) -> str:
        """
            This function demonstrates how to invoke an Amazon Bedrock model to get movie recommendations based on user input.
            :param input: A string containing the user input.
            :return: A string containing movie recommendations.
            """

        # Set the model ID, e.g., Amazon Titan Text G1 - Express.
        model_id = "amazon.titan-text-express-v1"

        # Define the prompt for the model.
        prompt = f"Recommend some movies based on the following user input: '{input}'"

        # Send the prompt to the model.
        response = self._invoke_model(prompt)

        print(f"Response: {response}")

        logger.info("Done.")

        return response
