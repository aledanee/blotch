from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    image_url: Optional[HttpUrl] = None  # Validate as URL but store as string
    text: str
    category_id: int
    is_published: bool = False
    read_time: Optional[int] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    views: int = 0


class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    views: int = 0

class SimplifiedArticleResponse(BaseModel):
    id: int
    title: str


    
    class Config:
        from_attributes = True
