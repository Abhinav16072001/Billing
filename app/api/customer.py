from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.customer import Customer, CustomerCreate, CustomerBase
from app.database.actions import create_customer_record, get_customers

router = APIRouter()

@router.post("/customers/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    data = create_customer_record(db, customer)
    return data

@router.get("/get_customers/")
def read_customer(db: Session = Depends(get_db)):
    customers = get_customers(db)
    if customers is None:
        raise HTTPException(status_code=404, detail="Customers not found")
    return customers
