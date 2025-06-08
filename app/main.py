import time
from typing import Optional, List
from fastapi import Body, FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from .database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils
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