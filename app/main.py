from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts=[{"title": "Title of post 1", "content": "Content of post 1", "published": True, "rating": 5, "id": 1},
           {"title": "Title of post 2", "content": "Content of post 2", "published": False, "rating": 3, "id": 2}]

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts}

@app.post("/posts")
def create_posts(post: Post, status_code=status.HTTP_201_CREATED):
    post_dict=post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

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
    post = find_post(id)
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
    idx= find_index_post(id)

    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Post not found"})
    
    my_posts.pop(idx)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    idx= find_index_post(id)

    if idx is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Post not found"})

    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[idx] = post_dict
    return {'message':"updated post"}