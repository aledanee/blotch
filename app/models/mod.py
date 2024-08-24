# models.py
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr

import enum

Base = declarative_base()



class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str  # Correctly annotate the type as 'str'
    created_at: datetime  # Correctly annotate the type as 'datetime'
    disabled: bool  # This is already correct


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRole(enum.Enum):
    owner = "owner"
    user = "user"


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

    class Config:
         from_attributes = True



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.user)
    created_at = Column(DateTime)
    disabled = Column(Boolean, default=False)  # Add this column

    articles = relationship("Article", back_populates="author")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")



class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="refresh_tokens")

User.refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete")


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime)

    articles = relationship("Article", back_populates="category")

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    image_url = Column(String(9999))
    text = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    views = Column(Integer, default=0)
    read_time = Column(Integer)

    category = relationship("Category", back_populates="articles")
    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article")
    likes = relationship("Like", back_populates="article")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    created_at = Column(DateTime)

    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)

    article = relationship("Article", back_populates="likes")
    user = relationship("User", back_populates="likes")

class Draft(Base):
    __tablename__ = 'drafts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    image_url = Column(String(255))
    text = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)

class Analytics(Base):
    __tablename__ = 'analytics'
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    created_at = Column(DateTime)




