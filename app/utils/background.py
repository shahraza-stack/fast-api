import time
import random
import json
from app.utils.redis_client import redis_client

def mock_model_predict(input: str) -> dict:
    time.sleep(random.randint(10, 17))  # Simulate processing delay
    result = {"input": input, "result": str(random.randint(1000, 20000))}
    return result

def process_prediction(prediction_id: str, input_data: str):
    """
    This function simulates a prediction and stores the result in Redis.
    """
    result = mock_model_predict(input_data)
    
    # Save the result to Redis (use JSON to store a dict)
    redis_client.hset("predictions", prediction_id, json.dumps(result))
