from fastapi import FastAPI
from config.database import engine
import config.models as models
from routers import user, post, auth, likes
from fastapi.middleware.cors import CORSMiddleware

# This is responsible for creating the models
models.Base.metadata.create_all(bind=engine)
# this wont work now cos its allembic thats doing it now

app = FastAPI()

# this is a list of domain that can access your domain
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allowed_origins=origins,
    allow_credentials=True,
    allow_method=["*"],
    allowed_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(likes.router)
