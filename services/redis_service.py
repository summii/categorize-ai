import os
import redis
import json
from config.base import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_EXPIRE_TIME
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RedisService:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST','localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True
            )
            self.default_expire_time = int(os.getenv('REDIS_EXPIRE_TIME', 3600))
        except Exception as e:
            print(f"Redis connection error: {e}")
            raise e

    def get_cache(self, key):
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    def set_cache(self, key , value, expire_time=REDIS_EXPIRE_TIME):
        try:
            self.redis_client.setex(
                key,
                expire_time,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    def delete_cache(self, key):
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False

