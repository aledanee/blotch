
# routers/like.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.like import LikeResponse
from app.crud.like import create_like, get_likes_by_article
from app.models.mod import Like, User
from app.routers.auth import get_current_active_user
from app.database.database import get_db

router = APIRouter()

@router.post("/articles/{article_id}/likes/", response_model=LikeResponse)
async def add_like(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return create_like(db, article_id, current_user.id)

@router.get("/articles/{article_id}/likes/", response_model=List[LikeResponse])
async def get_likes(article_id: int, db: Session = Depends(get_db)):
    return get_likes_by_article(db, article_id)