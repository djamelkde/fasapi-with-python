from pydantic import BaseModel, EmailStr
from datetime import datetime

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
    #config class is used to tell pandantic model to use other orm models other than dict
    class Config:
        orm_mode = True

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