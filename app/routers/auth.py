from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated, List, Optional, Union

from app.models.mod import User, Token, TokenData, UserCreate, UserResponse, UserRole, UserUpdate
from app.database.database import get_db

# JWT and OAuth2 configurations
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/token")

router = APIRouter()

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user

def authenticate_user_by_email(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return False
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)  # We use email instead of username
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.username)  # Fetch user by email
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# API routes
@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user_by_email(db, form_data.username, form_data.password)  # Authenticate by email
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires  # Use email in the token
    )
    return {"access_token": access_token, "token_type": "bearer"}
    


@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

# @router.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]


# Password context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        created_at=datetime.utcnow(),
        disabled=False  # Set default value for new users
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    new_user = create_user(db, user)
    return new_user




# User Management Endpoints



@router.put("/users/", response_model=UserResponse)
async def update_user(
    user_identifier: Union[int, str],
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    # Determine if the user_identifier is user_id (int), email (str with "@"), or username (str)
    if isinstance(user_identifier, int):
        db_user = db.query(User).filter(User.id == user_identifier).first()
    elif "@" in user_identifier:
        db_user = db.query(User).filter(User.email == user_identifier).first()
    else:
        db_user = db.query(User).filter(User.username == user_identifier).first()
    
    # If no user is found, raise an exception
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Check if the new username is already in use by another user
    if user_update.username:
        username_in_use = db.query(User).filter(User.username == user_update.username).first()
        if username_in_use and username_in_use.id != User:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use")
    

    # Check if the new email is already in use by another user
    if user_update.email:
        email_in_use = db.query(User).filter(User.email == user_update.email).first()
        if email_in_use and email_in_use.id != User:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    

    # Update the user's information based on provided data
    if user_update.username:
        db_user.username = user_update.username
    if user_update.email:
        db_user.email = user_update.email
    if user_update.role:
        db_user.role = user_update.role
    
    # Commit the changes to the database
    db.commit()
    db.refresh(db_user)
    return db_user




@router.get("/users/", response_model=List[UserResponse])
async def get_users(
    email: Optional[str] = None,
    username: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if email:
        query = query.filter(User.email == email)
    if username:
        query = query.filter(User.username == username)
    if start_date:
        query = query.filter(User.created_at >= start_date)
    if end_date:
        query = query.filter(User.created_at <= end_date)

    users = query.order_by(User.id).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    return users