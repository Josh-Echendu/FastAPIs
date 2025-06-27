from typing import List
from fastapi import Body, Depends, APIRouter, FastAPI, HTTPException, status
from config.database import engine, get_db
import config.models as models
from sqlalchemy.orm import Session
from  config.schemas import AllUser, CreateUsers, UserResponse
from config.utils import hash_method

router = APIRouter()
@router.get("/all_users", response_model=List[AllUser])
 #  db: Session = Depends(get_db): this create a session to the database so, we could communicate with the database
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    print(users)
    return users

# Create a new User
@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_post(user: CreateUsers, db: Session = Depends(get_db)):
    new_user = user.model_dump()
    hashed_password = hash_method(new_user.get('password')) 
    
    # updating existing password with new hashed password 
    new_user['password'] = hashed_password
    new_user = models.Users(**new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get a particular User
@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with {id}, does not exist')
    
    return user

