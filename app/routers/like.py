from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, OAuth2

router = APIRouter(
    prefix= "/likes",
    tags= ["Like"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def make_like(like: schemas.Like, db: Session = Depends(database.get_db), current_user = Depends(OAuth2.get_current_user)):

    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()
    print(found_like)
    if like.dir == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has aleady liked the post {like.post_id}")
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Successfully added like"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Like with post {like.post_id} related to User {current_user.id} does not exist")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully like deleted"}
