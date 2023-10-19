from fastapi import FastAPI
from app.api import customer

app = FastAPI()

app.include_router(customer.router)
