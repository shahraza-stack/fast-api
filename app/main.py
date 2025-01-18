from fastapi import FastAPI
from app.routes import predictions

app = FastAPI()

# Include prediction routes
app.include_router(predictions.router)
