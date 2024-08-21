#!/bin/bash

# Create project directory
#mkdir blog_project
#cd blog_project

# Create virtual environment
#python3 -m venv .venv
#source .venv/bin/activate

# Install necessary packages
#pip install fastapi uvicorn sqlalchemy alembic 'passlib[bcrypt]' 'python-jose[cryptography]' mysql-connector-python jwt

# Create directory structure
mkdir app
mkdir app/models
mkdir app/schemas
mkdir app/routers
mkdir app/crud
mkdir app/database
mkdir app/utils

# Create necessary files
touch app/main.py
touch app/models/__init__.py
touch app/models/user.py
touch app/models/article.py
touch app/schemas/__init__.py
touch app/schemas/user.py
touch app/schemas/article.py
touch app/routers/__init__.py
touch app/routers/user.py
touch app/routers/article.py
touch app/crud/__init__.py
touch app/crud/user.py
touch app/crud/article.py
touch app/database/__init__.py
touch app/database/database.py
touch app/utils/security.py
touch alembic.ini
mkdir alembic
mkdir alembic/versions

# Add basic content to main.py
echo "from fastapi import FastAPI
from app.routers import user, article

app = FastAPI()

app.include_router(user.router)
app.include_router(article.router)

@app.get('/')
def read_root():
    return {'Hello': 'World'}
" > app/main.py

# Basic database.py content
echo "from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql+mysqlconnector://user:password@localhost/db_name'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
" > app/database/database.py

# Alembic init
alembic init alembic

echo "Project structure created and basic setup done."

