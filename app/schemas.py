from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

###### Pydantic model for user ############
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    creation_date: datetime
    #config class is used to tell pandantic model to use other orm models other than dict
    class Config:
        orm_mode = True

############ Pydantic model for User Login ##############
class UserLogin(CreateUser):
    pass

#scheme of the RestAPI methods for request & response content
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    creation_date: datetime
    user_id : int
    #config class is used to tell pandantic model to use other orm models other than dict
    owner: UserResponse
    class Config:
        orm_mode = True

################## pydantic model for Like ###############
class Like(BaseModel):
    post_id: int
    dir: conint(le=1)

################## pydantic model for access jwt token ###############
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None