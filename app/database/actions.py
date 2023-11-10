from sqlalchemy.orm import Session
from .base import Userdb
from app.models.user import User


def create_user(db: Session, user_data: User):
    new_user = Userdb(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session):
    customers = db.query(Userdb).all()
    return customers


def user_exists(db: Session, username: str):
    user = db.query(Userdb).filter(Userdb.username == username).first()
    if user:
        return True
    return None


def user_role_exists(db: Session, username: str, role: str):
    user = db.query(User).filter(User.username == username, User.role == role).first()
    print(user)
    if user:
        return True
    return None


def get_userinfo(db: Session, username: str):
    user = db.query(Userdb).filter(Userdb.username == username).first()
    return user
