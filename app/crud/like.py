# crud/like.py
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.mod import Like
from app.schemas.like import LikeCreate

# def create_like(db: Session, article_id: int, user_id: int):
#     db_like = Like(article_id=article_id, user_id=user_id, created_at=datetime.utcnow())
#     db.add(db_like)
#     db.commit()
#     db.refresh(db_like)
#     return db_like

def create_like(db: Session, article_id: int, user_id: int):
    # Check if the like already exists
    existing_like = db.query(Like).filter_by(article_id=article_id, user_id=user_id).first()

    if existing_like:
        # If like exists, remove it (unlike)
        db.delete(existing_like)
        db.commit()
        return {
            "id": existing_like.id,
            "article_id": article_id,
            "user_id": user_id,
            "created_at": existing_like.created_at,
            "message": "Like removed"
        }
    else:
        # If like does not exist, create a new like
        new_like = Like(article_id=article_id, user_id=user_id, created_at=datetime.utcnow())
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return new_like

def get_likes_by_article(db: Session, article_id: int):
    return db.query(Like).filter(Like.article_id == article_id).all()