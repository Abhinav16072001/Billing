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


router = APIRouter(prefix='/admin', tags=['admin'])


@router.get("/dashboard")
async def dashboard(
    current_user: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_db)
):
    user_info = get_userinfo(db, username=current_user.username)
    return user_info
