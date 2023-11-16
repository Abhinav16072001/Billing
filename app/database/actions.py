from typing import List
from sqlalchemy.orm import Session
from .base import *
from app.models.user import User
from app.models.test import TestCreate, QuestionBase, OptionBase

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
