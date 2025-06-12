from typing import List
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from config.db import engine, get_db
import config.models as models
from sqlalchemy.orm import Session
from config.schemas import CreatePost, CreateUsers, PostResponse, UserResponse
from config.utils import hash_method
from routers import user, post, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='qwerty12345', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successfull")
        break
    except Exception as e:
        print("connection Failed: ", e)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
