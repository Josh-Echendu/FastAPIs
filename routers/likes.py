from typing import List, Optional
from fastapi import Body, Depends, HTTPException, Response, status, APIRouter
from config.database import engine, get_db
from config import models
from sqlalchemy.orm import Session
from config.schemas import Likes, LikesResponse # Ensure LikesResponse is imported
from routers import oauth2
# from config.models import Like # This is redundant if models is already imported

router = APIRouter()

@router.post('/likes_post', response_model=LikesResponse)
def like_post(
    vote: Likes,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(oauth2.get_current_user)
):
    current_user_id = current_user.id

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {vote.post_id} does not exist.")

    existing_entry = db.query(models.Like).filter(
        models.Like.user_id == current_user_id,
        models.Like.post_id == vote.post_id
    ).first()

    try:
        if existing_entry:
            if existing_entry.liked == vote.liked:
                # Toggle off like
                existing_entry.liked = False
            else:
                existing_entry.liked = vote.liked
            db.commit()
            db.refresh(existing_entry)
            return existing_entry
        else:
            new_like = models.Like(user_id=current_user_id, post_id=vote.post_id, liked=vote.liked)
            db.add(new_like)
            db.commit()
            db.refresh(new_like)
            return new_like

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected server error occurred: {e}"
        )
