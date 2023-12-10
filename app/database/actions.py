from typing import List
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import insert
from .base import *
from app.models.user import User
from app.models.test import TestCreate, QuestionBase
from app.models.items import MenuItemCreate

# User


def create_user(db: Session, user_data: User):
    """
    Create a new user in the database.

    Args:
    - db (Session): Database session
    - user_data (User): User data to be added

    Returns:
    - Userdb: Newly created user object
    """
    new_user = Userdb(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session):
    """
    Retrieve all users from the database.

    Args:
    - db (Session): Database session

    Returns:
    - list: List of all users in the database
    """
    users = db.query(Userdb).all()
    return users


def user_exists(db: Session, username: str):
    """
    Check if a user exists in the database.

    Args:
    - db (Session): Database session
    - username (str): Username to be checked

    Returns:
    - bool or None: True if the user exists, else None
    """
    user = db.query(Userdb).filter(Userdb.username == username).first()
    return bool(user)


def user_role_exists(db: Session, username: str, role: str):
    """
    Check if a user with a specific role exists in the database.

    Args:
    - db (Session): Database session
    - username (str): Username to be checked
    - role (str): Role to be checked for the user

    Returns:
    - bool or None: True if the user with the role exists, else None
    """
    user = db.query(User).filter(User.username ==
                                 username, User.role == role).first()
    return bool(user)


def get_userinfo(db: Session, username: str):
    """
    Retrieve user information by username.

    Args:
    - db (Session): Database session
    - username (str): Username to retrieve user information

    Returns:
    - Userdb: User information based on the provided username
    """
    user = db.query(Userdb).filter(Userdb.username == username).first()
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve a user by their ID from the database.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user corresponding to the given ID.
    """
    return db.query(Userdb).filter(Userdb.id == user_id).first()


def change_user_disable_status(db: Session, username: str, disabled: bool) -> bool:
    """
    Change the 'disabled' status of a user in the database.

    Args:
        db (Session): SQLAlchemy database session.
        username (str): Username of the user whose status is to be changed.
        disabled (bool): New status for the 'disabled' field.

    Returns:
        bool: True if the user's status was updated successfully, False otherwise.
    """
    user = db.query(Userdb).filter(Userdb.username == username).first()
    if user:
        user.disabled = disabled
        db.commit()
        return True  # Indicates successful update
    return False  # User not found


# Test


def create_test_record(db: Session, test_data: TestCreate) -> Test:
    """
    Create a new test record in the database.

    Args:
        db (Session): Database session.
        test_data (TestCreate): Data for creating a new test.

    Returns:
        Test: The created test object.
    """
    db_test = Test(title=test_data.title, description=test_data.description)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


def create_questions(db: Session, test_id: int, questions: List[QuestionBase]):
    """
    Create questions and corresponding options for a specific test.

    Args:
        db (Session): Database session.
        test_id (int): ID of the test.
        questions (List[QuestionBase]): List of question data.

    Returns:
        List[Question]: List of created question objects.
    """
    created_questions = []
    for question_data in questions:
        db_question = Question(text=question_data.text, test_id=test_id)
        db.add(db_question)
        db.commit()

        db.refresh(db_question)
        created_questions.append(db_question)

        options = []
        for option_data in question_data.options:
            db_option = Option(**option_data.dict(),
                               question_id=db_question.id)
            options.append(db_option)

        db.add_all(options)
        db.commit()

    return created_questions


def get_test_by_id(db: Session, test_id: int) -> Test:
    """
    Retrieve a test by its ID.

    Args:
        db (Session): Database session.
        test_id (int): ID of the test.

    Returns:
        Test: The test object corresponding to the ID.
    """
    return db.query(Test).filter(Test.id == test_id).first()


# Assigned

def get_assigned_tests_for_user(db: Session, user: User) -> list:
    """
    Retrieve tests assigned to a specific user from the database.

    Args:
        db (Session): The database session.
        user (User): The user for whom tests are to be retrieved.

    Returns:
        list: A list of Test objects assigned to the user.
    """
    assigned_tests = (
        db.query(Test, user_test_association.c.created_at, user_test_association.c.start_time,
                 user_test_association.c.end_time, user_test_association.c.duration, user_test_association.c.is_expired)
        .join(user_test_association)
        .filter(user_test_association.c.user_id == user.id)
        .all()
    )

    assigned_tests_with_timestamp = [
        {
            "title": test.title,
            "assigned_at": timestamp,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "is_expired": is_expired
        }
        for test, timestamp, start_time, end_time, duration, is_expired in assigned_tests
    ]

    return assigned_tests_with_timestamp


def create_user_test_assignment(db, user_ids, test_ids, start_time, end_time):
    for user_id in user_ids:
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=404, detail=f"User with ID {user_id} not found")

        for test_id in test_ids:
            test = get_test_by_id(db, test_id)
            if not test:
                raise HTTPException(
                    status_code=404, detail=f"Test with ID {test_id} not found")

            # Calculate duration_minutes using datetime objects
            duration_minutes = (end_time - start_time).total_seconds() // 60

            # Check if the test is already assigned to the user
            if test not in user.tests:
                # Append the test with time-related info to user.tests
                assignment_values = {
                    'user_id': user.id,
                    'test_id': test.id,
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': duration_minutes,
                    'is_expired': False
                }

                # Create an INSERT statement and execute it
                insert_stmt = insert(user_test_association).values(
                    **assignment_values)
                db.execute(insert_stmt)

    db.commit()  # Commit the changes
    return {"message": "UserTestAssignments created successfully"}


# Menu

def create_menu_item_in_db(db: Session, user_id: int, menu_item: MenuItemCreate):
    """
    Create a new menu item in the database for a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user associated with the menu item.
        menu_item (MenuItemCreate): Details of the menu item to be created.

    Returns:
        MenuItemDb: The created menu item in the database.
    """
    db_menu_item = MenuItemDb(
        name=menu_item.name,
        description=menu_item.description,
        price=menu_item.price,
        image_url=menu_item.image_url,
        category=menu_item.category,
        user_id=user_id  # Assuming user_id is the foreign key linking MenuItem to User
    )
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item
