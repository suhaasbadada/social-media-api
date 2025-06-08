from fastapi import  FastAPI
from dotenv import load_dotenv
import os
from .database import engine
from . import models
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}