import boto3
import json
from app.core.config import settings

class BedrockService:
    def __init__(self):
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.AWS_REGION
        )

    async def generate_response(self, prompt: str, system_prompt: str = ""):
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })

        response = self.client.invoke_model(
            body=body,
            modelId=settings.BEDROCK_MODEL_ID
        )

        response_body = json.loads(response.get("body").read())
        return response_body.get("content")[0].get("text")

    async def get_embeddings(self, text: str):
        body = json.dumps({
            "inputText": text
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId=settings.BEDROCK_EMBEDDING_MODEL_ID
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("embedding")
