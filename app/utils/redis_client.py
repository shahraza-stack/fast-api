import os
import redis

redis_host = os.getenv("REDIS_HOST", "redis") 
redis_port = os.getenv("REDIS_PORT", 6379)  
# Creat a Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
