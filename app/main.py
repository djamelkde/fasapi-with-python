from operator import mod
from statistics import mode
from turtle import pos, title
from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
import fastapi
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# connection to the database
while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", 
                                port="5433", password="esiINIdjMI21", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successfull :)")
        break
    except Exception as error:
        print("Connection to databse failed :(")
        print("error: ", error)
        time.sleep(2)


#for now we store our posts in the memory
my_posts = [{"title": "title of the post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like couscous", "id": 2}]

#GET methods
@app.get("/")
async def root():
    return {"message": "Simple FastAPI with Python3"}

#get the latest post
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) -1 ]
    return post

#get all the posts
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

#get a specific post using its id
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() # we know there is only one output
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return post

#POST methods
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", 
    #                (new_post.title, new_post.content, new_post.published))
    # post = cursor.fetchone()
    # conn.commit()
    #print(**new_post.dict())
    #post = models.Post(title=new_post.title, content= new_post.content, published = new_post.published)
    post = models.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


#PUT methods
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING*""", (new_post.title, new_post.content, str(new_post.published), str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


#DELETE methods
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
