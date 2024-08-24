from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers import auth as auth_user, comment, like
from app.routers import category as category
from app.routers import article
from fastapi.middleware.cors import CORSMiddleware
import os
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
    allow_origins=["*"],  # Or specify the allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_user.router, prefix="/v1", tags=["users"])
app.include_router(category.router, prefix="/v1", tags=["categories"])
app.include_router(article.router, prefix="/v1", tags=["articles"])
app.include_router(comment.router, prefix="/v1/comment", tags=["interacte"])
app.include_router(like.router, prefix="/v1/like", tags=["interacte"])



# If you don't need to serve static files, remove this line:
# app.mount("/static", StaticFiles(directory="blotch/app/static"), name="static")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Endpoint to serve the home.html file
@app.get("/home")
async def get_home():
    file_path = "app/home.html"  # Adjust the path to match your project structure
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}
    


@app.get('/')
def read_root():
    return {'Hello': 'World'}
