from typing import List
from fastapi import Body, Depends, HTTPException, Response, status, APIRouter
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from config.db import engine, get_db
import config.models as models
from sqlalchemy.orm import Session
from config.schemas import CreatePost, PostResponse
from routers import oauth2

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

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


@router.get("/sqlalchemy", response_model=List[PostResponse])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts

@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    post_data = post.model_dump()
    new_post = models.Post(**post_data)
    db.add(new_post)            # Add to session
    db.commit()                 # Commit the transaction
    db.refresh(new_post)        # Refresh and retrieve the new instance(post) to get the new ID
    return new_post


@router.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return result

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    result = db.query(models.Post).filter(models.Post.id == id)

    if result.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    result.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/posts/{id}', response_model=PostResponse)
def update_post(id: int, post: CreatePost, db: Session = Depends(get_db)):
    
    # Build a query to search for the post with the given ID
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    # Execute the query to get the first result (i.e., the post object if it exists)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    # synchronize_session=False improves performance by skipping session sync
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


