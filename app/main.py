from fastapi import FastAPI
from .config.database import engineconn

from .models.models import Base

app = FastAPI()

engine = engineconn()
session = engine.sessionmaker()

Base.metadata.create_all(bind=engine.engine)


@app.get("/")
async def first_get():
    print("Hello")
