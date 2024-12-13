from fastapi import FastAPI
from .predict import predict_endpoint

app = FastAPI()

# Include routes
app.include_router(predict_endpoint)
