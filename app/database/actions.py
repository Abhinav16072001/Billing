from sqlalchemy.orm import Session
from .base import Customerdb
from app.models.customer import CustomerCreate

def create_customer_record(db: Session, customer_data: CustomerCreate):
    db_customer = Customerdb(**customer_data.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customers(db: Session):
    customers = db.query(Customerdb).all()
    return customers
