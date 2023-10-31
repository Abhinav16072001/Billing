from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database.security import *
from app.database.actions import *
from app.database.session import get_db
from app.models.token import Token
from app.models.user import User, CreateUserRequest

router = APIRouter(prefix='/user', tags=['user'])


@router.post("/create_user")
def create_user_data(user_data: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        existing_user = user_exists(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=400, detail="User with this username already exists")

        hashed_password = get_password_hash(user_data.password)
        user_in_db = UserInDB(**user_data.dict(),
                              hashed_password=hashed_password)

        db_user = create_user(db, user_in_db)

        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/users")
def get_user_info(db: Session = Depends(get_db)):
    try:
        users = get_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
