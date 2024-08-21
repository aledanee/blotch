# schemas/comment.py
from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    article_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True