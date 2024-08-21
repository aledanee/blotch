# schemas/like.py
from pydantic import BaseModel
from datetime import datetime

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    pass

class LikeResponse(LikeBase):
    id: int
    article_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True