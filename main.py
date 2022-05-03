from re import I
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import fastapi
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#scheme of the post/put request
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #the default value is True if it is not provided by the user
    rating: Optional[int] = None

#for now we store our posts in the memory
my_posts = [{"title": "title of the post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like couscous", "id": 2}]

#GET methods
@app.get("/")
async def root():
    return {"posts": "hello world"}

#get all the posts
@app.get("/posts")
def get_posts():
    return {"posts": my_posts}

#get the latest post
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) -1 ]
    return {"post_details": post}

#get a specific post using its id
@app.get("/posts/{id}")
def get_post(id: int, response: fastapi.Response):
    post = find_one_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {"post_details": post}

#POST methods
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post = new_post.dict()
    print(post)
    post["id"] = randrange(1, 10000000)
    my_posts.append(post)
    #return {"new_post": f"title {payload['title']} content: {payload['content']}"}
    return {"data": post}


#PUT methods
@app.put("/posts/{id}")
def update_post(id: int, new_post : Post):
    index = find_index_of_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post = new_post.dict()
    post["id"] = id
    my_posts[index] = post
    return {"data": post}



#DELETE methods
@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index_of_post(id)
    if index != None:
        my_posts.pop(index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    


#helper functions
def find_one_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

#find the index of the post whose id is {id}
def find_index_of_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None