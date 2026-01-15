import redis
import json
import boto3
from datetime import datetime, timedelta
from app.core.config import settings

class MemoryService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST, 
            port=settings.REDIS_PORT, 
            db=0,
            decode_responses=True
        )
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION)
        self.s3 = boto3.client('s3', region_name=settings.AWS_REGION)

    async def get_memory(self, user_id: str, session_id: str):
        # 1. Check Caching Layer (Popular/Recent responses)
        # 2. Check Temp Memory (Redis - 8h)
        temp_mem = self.redis_client.get(f"session:{session_id}")
        if temp_mem:
            return json.loads(temp_mem)

        # 3. Check Short-term Memory (DynamoDB - 7 days)
        # (Simplified implementation)
        st_mem = self._get_dynamo_memory(user_id)
        return st_mem

    async def save_memory(self, user_id: str, session_id: str, message: dict):
        # Save to Temp (Redis - 8h TTL)
        self.redis_client.setex(
            f"session:{session_id}",
            timedelta(hours=8),
            json.dumps(message)
        )

        # Save to Short-term (DynamoDB - TTL 7 days)
        self._save_to_dynamo(user_id, message)

        # Save to Long-term (S3 for fine-tuning)
        self._save_to_s3(user_id, message)

    def _save_to_dynamo(self, user_id, message):
        # DynamoDB table 'UserChatHistory'
        table = self.dynamodb.Table('UserChatHistory')
        ttl = int((datetime.now() + timedelta(days=7)).timestamp())
        table.put_item(Item={
            'UserId': user_id,
            'Timestamp': datetime.now().isoformat(),
            'Message': message,
            'TTL': ttl
        })

    def _save_to_s3(self, user_id, message):
        # For long-term storage and future fine-tuning
        key = f"chats/{user_id}/{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        self.s3.put_object(
            Bucket='llmops-long-term-memory',
            Key=key,
            Body=json.dumps(message)
        )

    def _get_dynamo_memory(self, user_id):
        table = self.dynamodb.Table('UserChatHistory')
        response = table.query(
            KeyConditionExpression='UserId = :uid',
            ExpressionAttributeValues={':uid': user_id},
            Limit=10,
            ScanIndexForward=False
        )
        return response.get('Items', [])
