# crud/comment.py
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.mod import Article, Comment
from app.schemas.comment import CommentCreate

def create_comment(db: Session, comment: CommentCreate, article_id: int, user_id: int):
    db_comment = Comment(**comment.dict(), article_id=article_id, user_id=user_id, created_at=datetime.utcnow())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_by_article(db: Session, article_id: int):
    return db.query(Comment).filter(Comment.article_id == article_id).all()

def create_comment(db: Session, comment: CommentCreate, article_id: int, user_id: int):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Article does not exist")

    db_comment = Comment(**comment.dict(), article_id=article_id, user_id=user_id, created_at=datetime.utcnow())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment