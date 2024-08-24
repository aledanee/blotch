from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.mod import Article, Category, Like, User
from app.database.database import get_db
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, SimplifiedArticleResponse
from app.routers.auth import get_current_active_user

router = APIRouter()

@router.post("/articles/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    
     # Check if the category exists
    category = db.query(Category).filter(Category.id == article.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    
    new_article = Article(
        title=article.title,
        image_url=str(article.image_url) if article.image_url else None,  # Convert HttpUrl to string
        text=article.text,
        category_id=article.category_id,
        author_id=current_user.id,
        is_published=article.is_published,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        read_time=article.read_time
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.get("/articles/test", response_model=List[ArticleResponse])
async def get_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()


@router.get("/search/articles/", response_model=List[ArticleResponse])
async def get_articles(
    search: Optional[str] = None,  # Query parameter for searching titles
    db: Session = Depends(get_db)
):
    query = db.query(Article)

    if search:
        search_query = f"%{search}%"
        query = query.filter(Article.title.ilike(search_query))

    articles = query.all()

    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")

    return articles

@router.get("/articles/all", response_model=List[ArticleResponse])
async def get_articles(
    category_id: Optional[int] = None,
    author_id: Optional[int] = None,
    is_published: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Article)

    if category_id:
        query = query.filter(Article.category_id == category_id)
    if author_id:
        query = query.filter(Article.author_id == author_id)
    if is_published is not None:
        query = query.filter(Article.is_published == is_published)

    articles = query.all()

    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")

    return articles

@router.get("/articles/", response_model=List[ArticleResponse])
async def get_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Article).offset(skip).limit(limit).all()

@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article

@router.put("/articles/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    if article.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this article")

    article.title = article_update.title
    article.image_url = article_update.image_url
    article.text = article_update.text
    article.category_id = article_update.category_id
    article.is_published = article_update.is_published
    article.updated_at = datetime.utcnow()
    article.read_time = article_update.read_time

    db.commit()
    db.refresh(article)
    return article

@router.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    
    if article.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this article")

    db.delete(article)
    db.commit()
    return {"detail": "Article deleted successfully"}

@router.get("/articles/most-liked", response_model=SimplifiedArticleResponse)
async def get_most_liked_article(db: Session = Depends(get_db)):
    most_liked_article = (
        db.query(Article)
        .join(Like, Like.article_id == Article.id)
        .group_by(Article.id)
        .order_by(func.count(Like.id).desc())
        .first()
    )

    if not most_liked_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No articles found")

    return most_liked_article

@router.get("/articles/latest", response_model=List[ArticleResponse])
async def get_latest_articles(limit: int = 3, db: Session = Depends(get_db)):
    """
    Get the latest articles ordered by creation date.
    """
    try:
        articles = (
            db.query(Article)
            .order_by(Article.created_at.desc())
            .limit(limit)
            .all()
        )

        if not articles:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No articles found")

        return articles
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/articles/latest/a", response_model=List[SimplifiedArticleResponse])
async def get_latest_articles(limit: int = 3, db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.created_at.desc()).limit(limit).all()
    print(articles)  # Add this to inspect the data
    return articles





