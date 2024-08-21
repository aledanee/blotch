from fastapi import FastAPI
from app.routers import auth as auth_user, comment, like
from app.routers import category as category
from app.routers import article
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8001",  # Change this to your frontend URL
    "http://localhost:3000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:3000",
    # Add any other domains that should be allowed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend's URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_user.router, prefix="/v1", tags=["users"])
app.include_router(category.router, prefix="/v1", tags=["categories"])
app.include_router(article.router, prefix="/v1", tags=["articles"])
app.include_router(comment.router, prefix="/v1/comment", tags=["interacte"])
app.include_router(like.router, prefix="/v1/like", tags=["interacte"])

@app.get('/')
def read_root():
    return {'Hello': 'World'}
