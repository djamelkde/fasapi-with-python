from pyexpat import model
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, OAuth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(database.get_db)):
    #user_credentials dic format is :
    # {
    #     "username": "adaraf",
    #     "password": "hahazee"   
    # }
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verifyPasswordHash(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    #create a JWT Token
    access_token = OAuth2.create_access_token(data = {"user_id": user.id}) 
    return {"access_token": str(access_token), "token_type": "bearer"}