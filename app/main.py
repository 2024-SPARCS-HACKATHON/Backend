from fastapi import FastAPI
from .config.database import engineconn
from app.routes.audio_route import router as audio_router

from .models.models import Base

app = FastAPI()

engine = engineconn()
session = engine.sessionmaker()

Base.metadata.create_all(bind=engine.engine)

app.include_router(audio_router, prefix="/audio")

@app.get("/")
async def first_get():
    print("Hello")
