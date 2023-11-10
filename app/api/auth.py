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
from app.database.security import *
from app.models.token import Token, SignupToken
from app.models.user import User

router = APIRouter(prefix='/auth', tags=['auth'])

with open('app/utility/config.yml', 'r') as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

permissions_data = yaml_data['permissions']


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Endpoint to generate an access token for a user.

    Args:
        form_data (OAuth2PasswordRequestForm): User credentials.

    Returns:
        dict: Access token and token type.

    Raises:
        HTTPException: If the provided credentials are incorrect.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create_permission")
async def permissions(user_data: SignupToken, db: Session = Depends(get_db)):
    """
    Endpoint to create permissions and generate an access token for a user.

    Args:
        user_data (SignupToken): User registration data.

    Returns:
        dict: Message, permissions, and access token.

    Raises:
        Exception: If an invalid role is provided.
    """
    try:
        scopes = permissions_data[user_data.role]
    except KeyError:
        raise Exception("Invalid role: {}".format(user_data.role))

    login_payload = OAuth2PasswordRequestForm(
        grant_type="password",
        username=user_data.username,
        password=user_data.password,
        scope=scopes,
    )

    token = await login_for_access_token(login_payload)

    return {"permissions": permissions_data[user_data.role], "token": token}


@router.get("/status/")
async def read_system_status(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Endpoint to read the system status.

    Args:
        current_user (User): Currently authenticated user.

    Returns:
        dict: System status.
    """
    return {"status": "ok"}
