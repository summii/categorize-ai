import sys
import os
import pytest

from config import REDIS_EXPIRE_TIME

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

# Load environment variables before importing RedisService
load_dotenv()

from services.redis_service import RedisService


@pytest.fixture
def redis_service():
    # Ensure Redis connection settings are available
    os.environ['REDIS_HOST'] = 'localhost'
    os.environ['REDIS_PORT'] = '6379'
    os.environ['REDIS_DB'] = '0'
    os.environ['REDIS_EXPIRE_TIME'] = '3600'
    
    service = RedisService()
    # Clear test database before running tests
    service.redis_client.flushdb()
    return service


def test_redis_service(redis_service):
    assert redis_service.redis_client.ping()

def test_set_get(redis_service):
    test_key = "test_key"
    test_value = "test_value"

    redis_service.set_cache(test_key, test_value)

    retrieved_value = redis_service.get_cache(test_key)
    assert retrieved_value == test_value

def test_redis_expire(redis_service):
    test_key = "test_key"
    test_value = "test_value"
    expire_time = 3600

    redis_service.set_cache(test_key, test_value, REDIS_EXPIRE_TIME)
    ttl = redis_service.redis_client.ttl(test_key)
    assert ttl <= REDIS_EXPIRE_TIME and ttl > 0
