import time
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

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
    rating: Optional[int] = None

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

my_posts=[{"title": "Title of post 1", "content": "Content of post 1", "published": True, "rating": 5, "id": 1},
            {"title": "Title of post 2", "content": "Content of post 2", "published": False, "rating": 3, "id": 2}]

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data":posts}

@app.post("/posts")
def create_posts(post: Post, status_code=status.HTTP_201_CREATED):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING id;""",
                   (post.title, post.content, post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data": new_post}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

@app.get("/posts/latest")
def get_latest_post():
    if not my_posts:
        return {"error": "No posts available"}
    latest_post = my_posts[-1]
    return {"post_detail": latest_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", str((id),))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Post not found"})
    return {"post_detail": post}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Post not found"})
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
                   (post.title, post.content, post.published, id))
    updated_post=cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Post not found"})

    return {'message':updated_post}