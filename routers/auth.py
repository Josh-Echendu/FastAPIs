#password:  Mimie@1419
from fastapi.security import OAuth2PasswordRequestForm
from config.utils import verify
from fastapi import APIRouter, Depends, HTTPException, status
from requests import Session
from websockets import Router
from config.db import get_db
from config import db, models
from config.schemas import UserLogin
from sqlalchemy.orm import Session
from routers.oauth2 import create_access_token

router = APIRouter()

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm, db: Session = Depends(get_db)): #user_credentials stores the username and password

    #Exreact first user that matches the email address
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # access the verify function which hashes and compare password
    authentication = verify(user_credentials.password, user.password)

    if not authentication:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # access the create_access_token function
    access_token = create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

