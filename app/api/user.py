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
from app.models.token import Token, SignupToken
from app.models.user import User, CreateUserRequest
from app.models.test import TestSchemaWithoutCorrectness
from app.api.auth import permissions

router = APIRouter(prefix='/user', tags=['user'])


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
    return db_user, token


@router.get("/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],  db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve information for the currently authenticated user.

    Args:
        current_user (User): Currently authenticated user.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        dict: User information for the authenticated user.
    """
    user_info = get_userinfo(db, username=current_user.username)
    return user_info


@router.get("/users")
def get_user_info(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    """
    Endpoint to retrieve information for all users.

    Args:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        List[dict]: Information for all users.

    Raises:
        HTTPException: If an internal server error occurs.
    """
    try:
        users = get_users(db)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/tests/{test_id}/", response_model=TestSchemaWithoutCorrectness)
def get_test_info(test_id: int, current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    """
    Retrieve test information excluding 'is_correct' field from options.

    Args:
        test_id (int): The ID of the test to retrieve.

    Returns:
        dict: Test information excluding 'is_correct' field from options.
    """
    test = get_test_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = []
    for question in test.questions:
        options = []
        for option in question.options:
            option_data = {
                "id": option.id,
                "text": option.text
            }
            options.append(option_data)

        question_data = {
            "id": question.id,
            "text": question.text,
            "options": options
        }
        questions.append(question_data)

    test_data = {
        "id": test.id,
        "title": test.title,
        "description": test.description,
        "questions": questions
    }
    return test_data


@router.get("/tests_assigned/")
def get_tests_assigned(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    user = get_userinfo(db, current_user.username)
    print(user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    assigned_tests = get_assigned_tests_for_user(db,user)

    return [
            {"title": test['title'], "assigned_at": test['assigned_at']} for test in assigned_tests
        ]
