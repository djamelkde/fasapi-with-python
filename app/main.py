from fastapi import FastAPI
from .database import engine
from . import models
from .routers import user, post, auth, like
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

#CORS domains authorized to connect to our API
#origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"] #open for public

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#include the routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

#GET methods
@app.get("/")
async def root():
    return {"message": "Simple FastAPI with Python3"}
