from fastapi import FastAPI

from app.clients import router as client_router
from app.trainers import router as trainer_router

app = FastAPI()

app.include_router(client_router)
app.include_router(trainer_router)