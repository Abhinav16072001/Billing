from sqlalchemy.orm import Session
from .base import Customerdb, Userdb
from app.models.customer import CustomerCreate
from app.models.user import User


def create_customer_record(db: Session, customer_data: CustomerCreate):
    db_customer = Customerdb(**customer_data.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customers(db: Session):
    customers = db.query(Customerdb).all()
    return customers


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


def get_userinfo(db: Session, username: str):
    user = db.query(Userdb).filter(Userdb.username == username).first()
    return user
