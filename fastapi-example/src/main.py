from fastapi import FastAPI
from src.settings import settings

app = FastAPI()

@app.get("/")
async def read_root():
    return settings.model_dump()
