from fastapi import FastAPI
from .database import engine
from . import models
from .routers import user, post, auth, like
from .config import settings


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

#include the routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

#GET methods
@app.get("/")
async def root():
    return {"message": "Simple FastAPI with Python3"}
