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
from app.models.test import TestCreate, Test, TestSchema, OptionSchema, QuestionSchema, TestUserAssignment
from app.models.user import User, UserAccessUpdate
from app.models.items import MenuItemCreate

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


@router.put("/accessedit")
async def disable_user(user_data: UserAccessUpdate, current_user: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_db)):
    """
    Endpoint to modify user access rights based on the provided data.
    Args:
        user_data (UserAccessUpdate): Data to update user access.
        current_user (User): Currently authenticated admin user.
        db (Session): SQLAlchemy database session.

    Returns:
        User: Updated user information.

    Raises:
        HTTPException: If the user to be updated is not found.
    """
    success = change_user_disable_status(
        db, user_data.username, user_data.disabled)
    if success:
        return {"message": f"User disabled status updated"}
    raise HTTPException(status_code=404, detail=f"User not found")


@router.post("/add_test/", response_model=Test)
async def add_test(
    test_data: TestCreate,
    current_user: Annotated[User, Depends(get_current_active_admin)],
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
def get_test(test_id: int, current_user: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_db)):
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


@router.post("/assign-tests/")
def assign_tests_to_users(test_user_assignment: TestUserAssignment, current_user: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_db)):
    create_user_test_assignment(db, test_user_assignment.user_id, test_user_assignment.test_id,
                                test_user_assignment.start_time, test_user_assignment.end_time)

    return {"message": "Tests assigned to users"}


@router.get("/tests_assigned/")
def get_tests_assigned_to_users(current_user: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_db)):
    users_with_tests = {}
    users = get_users(db)

    for user in users:
        assigned_tests = get_assigned_tests_for_user(db, user)
        users_with_tests[user.username] = [
            test for test in assigned_tests
        ]

    return users_with_tests


@router.post("/addItems/")
def create_menu_item(menu_item: MenuItemCreate, current_user: Annotated[User, Depends(get_current_active_admin)], db: Session = Depends(get_db)):
    user = get_userinfo(db, current_user.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    created_item = create_menu_item_in_db(db, user.id, menu_item)
    return {"message": "Menu item added successfully", "data": created_item}
