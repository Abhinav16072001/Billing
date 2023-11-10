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
from app.models.token import Token, SignupToken, LoginToken
from app.models.user import User, CreateUserRequest
from app.api.auth import permissions, login_for_access_token

router = APIRouter(prefix='/gateway', tags=['gateway'])

with open('app/utility/config.yml', 'r') as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

permissions_data = yaml_data['permissions']


@router.post("/signup")
async def create_user_data(user_data: CreateUserRequest, db: Session = Depends(get_db)):
    """
    Endpoint to create a new user and generate permissions.

    Args:
        user_data (CreateUserRequest): User registration data.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        Tuple: Newly created user and authentication token.

    Raises:
        HTTPException: If a user with the same username already exists.
    """
    existing_user = user_exists(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this username already exists")

    hashed_password = get_password_hash(user_data.password)
    user_in_db = UserInDB(**user_data.dict(),
                          hashed_password=hashed_password)

    db_user = create_user(db, user_in_db)

    signup_payload = SignupToken(
        username=user_data.username,
        password=user_data.password,
        role=user_data.role,
    )
    token = await permissions(signup_payload)
    return {"message": "User registered successfully", "User": db_user, "token": token}


@router.post("/login")
async def create_user_data(user_data: LoginToken, db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user and generate an access token.

    Args:
        user_data (LoginToken): User login credentials.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        dict: Authentication token.

    Raises:
        HTTPException: If the user is not found or the provided credentials are incorrect.
    """
    existing_user = get_userinfo(db, user_data.username)

    if existing_user is None or existing_user.role != user_data.role:
        raise HTTPException(
            status_code=404, detail="User not found")

    try:
        scopes = permissions_data[existing_user.role]
    except KeyError:
        raise Exception("Invalid role: {}".format(user_data.role))

    login_payload = OAuth2PasswordRequestForm(
        grant_type="password",
        username=user_data.username,
        password=user_data.password,
        scope=scopes,
    )

    token = await login_for_access_token(login_payload)

    return token
