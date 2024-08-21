# routers/comment.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentResponse
from app.crud.comment import create_comment, get_comments_by_article
from app.models.mod import Comment, User
from app.routers.auth import get_current_active_user
from app.database.database import get_db

router = APIRouter()

@router.post("/articles/{article_id}/comments/", response_model=CommentResponse)
async def add_comment(
    article_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return create_comment(db, comment, article_id, current_user.id)

@router.get("/articles/{article_id}/comments/", response_model=List[CommentResponse])
async def get_comments(article_id: int, db: Session = Depends(get_db)):
    return get_comments_by_article(db, article_id)
