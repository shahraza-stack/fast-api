from fastapi import APIRouter, HTTPException, BackgroundTasks, Header
from pydantic import BaseModel
import uuid
import json
from app.utils.background import process_prediction, redis_client

router = APIRouter()

class PredictionRequest(BaseModel):
    input: str

@router.post("/predict")
async def predict(request: PredictionRequest, background_tasks: BackgroundTasks, async_mode: bool = Header(False)):
    prediction_id = str(uuid.uuid4())

    # If async_mode is true
    if async_mode:
        background_tasks.add_task(process_prediction, prediction_id, request.input)
        return {"message": "Request received. Processing asynchronously.", "prediction_id": prediction_id}

    # Synchronous processing
    result = {"input": request.input, "result": str(uuid.uuid4().int % 10000)}
    return result

@router.get("/predict/{prediction_id}")
async def get_prediction(prediction_id: str):
    # Retrieve the prediction result from Redis
    result = redis_client.hget("predictions", prediction_id)
    if not result:
        # Check if prediction is still being processed
        processing = redis_client.hget("predictions_status", prediction_id)
        if processing:
            raise HTTPException(
                status_code=400,
                detail="Prediction is still being processed."
            )
        else:
            # If no result and no processing flag
            raise HTTPException(
                status_code=404,
                detail="Prediction ID not found."
            )
    
    # If prediction is found
    return json.loads(result)