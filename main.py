from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #the default value is True if it is not provided by the user
    rating: Optional[int] = None

#for now we store our posts in the memory
my_posts = [{"title": "title of the post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like couscous", "id": 2}]


@app.get("/")
async def root():
    return {"posts": "hello world"}

@app.get("/posts")
def get_posts():
    return {"posts": my_posts}



@app.post("/posts")
def create_posts(new_post: Post):
    post = new_post.dict()
    print(post)
    post["id"] = randrange(1, 10000000)
    my_posts.append(post)
    #return {"new_post": f"title {payload['title']} content: {payload['content']}"}
    return {"data": post}

#the structure of a post : {title str, content str}