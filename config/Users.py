from typing import List
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from config.db import engine, get_db
import config.models as models
from sqlalchemy.orm import Session
from config.schemas import newUsers
from main import databaseConnection

app = FastAPI()

conn = databaseConnection()
if not conn:
    print("database connection failed")
    
@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_post(user: newUsers, db: Session = Depends(get_db)):
    new_user = user.model_dump()
    new_user = models.Users(**new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user