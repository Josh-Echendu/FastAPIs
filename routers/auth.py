from fastapi.security import OAuth2PasswordRequestForm
from config.utils import verify
from fastapi import APIRouter, Depends, HTTPException, status
from config.database import get_db
from config import models, schemas
from sqlalchemy.orm import Session
from routers.oauth2 import create_access_token
from config import schemas

router = APIRouter()

@router.post("/login", response_model=schemas.Token)

#OAuth2PasswordRequestForm: is retrieves user credentials
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(OAuth2PasswordRequestForm)
    
    # Extract user with matching email (OAuth2PasswordRequestForm uses 'username' for email/username)
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    
    # Verify password
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Generate access token
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
