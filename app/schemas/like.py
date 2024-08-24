# schemas/like.py
from pydantic import BaseModel
from datetime import datetime

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    pass

class LikeResponse(BaseModel):
    id: int
    article_id: int
    user_id: int
    created_at: datetime
    message: str = None  # Optional message field

    class Config:
        from_attributes = True