from typing import List, Optional
from fastapi import Body, Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func
from config.database import engine, get_db
from config import models
from sqlalchemy.orm import Session
from config.schemas import CreatePost, PostLikesResponse, PostResponse
from routers import oauth2

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.get("/sqlalchemy", response_model=List[PostLikesResponse])
 #  db: Session = Depends(get_db): this create a session to the database so, we could communicate with the database
def test_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
    search: Optional[str] = ""):
    print("user email: ", current_user.email)
    print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.icontains(search)).limit(limit).offset(skip).all()
    
    # joining both posts and likes table and grouping by post.id to get the amount of likes for each post
    posts_likes = db.query(models.Post, func.count(models.Like.liked).label('likes')).join(
        models.Like, models.Post.id == models.Like.post_id,
        isouter=True).filter(models.Like.liked == True).group_by(models.Post.id).all()
    print(posts_likes)
    jo = [{"Post": post, "likes": likes} for post, likes in posts_likes]
    print(jo)
    
    return posts_likes


@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
 #  db: Session = Depends(get_db): this create a session so that we could communicated with the datavbase
def create_posts(post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("user email: ", current_user.email)
    post_data = post.model_dump()
    new_post = models.Post(user_id = current_user.id, **post_data)
    db.add(new_post)            # Add to session
    db.commit()                 # Commit the transaction
    db.refresh(new_post)        # Refresh and retrieve the new instance(post) to get the new ID
    return new_post


@router.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("user email: ", current_user.email)
    result = db.query(models.Post).filter(models.Post.id == id, models.Post.user_id == current_user.id).first()
    
    print(result)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return result

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("user email: ", current_user.email)
    
    post_query = db.query(models.Post).filter(models.Post.id == id, models.Post.user_id == current_user.id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} does not exist")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put('/posts/{id}', response_model=PostResponse)
def update_post(id: int, post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("user email: ", current_user.email)

    # Build a query to search for the post with the given ID
    post_query = db.query(models.Post).filter(models.Post.id == id, models.Post.user_id == current_user.id)
    
    # Execute the query to get the first result (i.e., the post object if it exists)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    # synchronize_session=False improves performance by skipping session sync
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
