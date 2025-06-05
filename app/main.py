import time
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from .database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from app import models

models.Base.metadata.create_all(bind=engine)

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
        cursor=conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Connecting to database failed")
        print("Error:",e)
        time.sleep(2)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
def get_posts(db:Session = Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db:Session = Depends(get_db)):
    new_post=models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db:Session = Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Post not found"})
    return {"post_detail": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Post not found"})

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db:Session = Depends(get_db)):
    post_query=db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Post not found"})
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return {'data':post_query.first()}