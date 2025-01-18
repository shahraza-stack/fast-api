from pydantic import BaseModel

class PredictionRequest(BaseModel):
    input: str
