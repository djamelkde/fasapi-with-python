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
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post, auth

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


#include the routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#GET methods
@app.get("/")
async def root():
    return {"message": "Simple FastAPI with Python3"}
