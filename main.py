from fastapi import FastAPI
from app.api import customer, mails

app = FastAPI()

app.include_router(customer.router)
app.include_router(mails.router)
