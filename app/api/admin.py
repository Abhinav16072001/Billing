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
from app.models.test import TestCreate, QuestionBase, OptionBase, Test, TestSchema, OptionSchema, QuestionSchema
from app.models.user import User, CreateUserRequest


router = APIRouter(prefix='/admin', tags=['admin'])


@router.get("/")
async def dashboard(
    current_user: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve information for the admin dashboard.

    Args:
        current_user (User): Currently authenticated admin user.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        dict: User information for the admin dashboard.

    Raises:
        HTTPException: If the current user is not an active admin.
    """
    user_info = get_userinfo(db, username=current_user.username)
    return user_info


@router.post("/add_test/", response_model=Test)
async def add_test(
    test_data: TestCreate,
    current_user: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new test along with its questions and options.

    Args:
        test_data (TestCreate): Data to create a new test.
        current_user (User, optional): Current user creating the test.
        db (Session, optional): Database session.

    Returns:
        Test: The created test with its details.
    """
    try:
        db_test = create_test_record(db, test_data)

        created_questions = create_questions(
            db, db_test.id, test_data.questions)

        return db_test
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating test: {str(e)}")


@router.get("/tests/{test_id}", response_model=TestSchema)
def get_test(test_id: int, db: Session = Depends(get_db)):
    """
    Retrieve test information including questions and options.

    Args:
        test_id (int): The ID of the test to retrieve.

    Returns:
        TestSchema: Test information including questions and options.
    """
    test = get_test_by_id(db, test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = []
    for question in test.questions:
        options = []
        for option in question.options:
            option_data = OptionSchema.from_orm(option)
            options.append(option_data)

        question_data = QuestionSchema(
            id=question.id,
            text=question.text,
            options=options
        )
        questions.append(question_data)

    test_data = TestSchema(
        id=test.id,
        title=test.title,
        description=test.description,
        questions=questions
    )
    return test_data
