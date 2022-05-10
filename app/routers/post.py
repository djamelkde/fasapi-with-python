from pyexpat import model
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
import sqlalchemy
from .. import models, schemas, utils, OAuth2
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#for now we store our posts in the memory
my_posts = [{"title": "title of the post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like couscous", "id": 2}]

#get the latest post
@router.get("/latest")
def get_latest_post():
    post = my_posts[len(my_posts) -1 ]
    return post

#get all the posts
#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user = Depends(OAuth2.get_current_user), 
              max_limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).filter(
    #                  models.Post.title.contains(search)).limit(max_limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(
                      models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(
                      models.Post.id).filter(models.Post.user_id == current_user.id).filter(
                      models.Post.title.contains(search)).limit(max_limit).offset(skip).all()
    #print(results)
    return posts

#get a specific post using its id
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(OAuth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first() # we know there is only one output
    post = db.query(models.Post, func.count(models.Like.post_id).label("likes")).join(
                      models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(
                    models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.Post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform requested actions")
    return post

#POST methods
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(OAuth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", 
    #                (new_post.title, new_post.content, new_post.published))
    # post = cursor.fetchone()
    # conn.commit()
    #print(**new_post.dict())
    #post = models.Post(title=new_post.title, content= new_post.content, published = new_post.published)
    post = models.Post(user_id=current_user.id, **new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


#PUT methods
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user= Depends(OAuth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING*""", (new_post.title, new_post.content, str(new_post.published), str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform requested actions")
    post_query.update(new_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


#DELETE methods
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(OAuth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform requested actions")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
