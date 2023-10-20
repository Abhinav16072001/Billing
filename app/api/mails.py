import yaml
from fastapi import APIRouter, HTTPException, Depends, WebSocket
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.customer import Customer, CustomerCreate, CustomerBase
from app.database.actions import create_customer_record, get_customers
from app.connections.mailing import *
from starlette.responses import JSONResponse

router = APIRouter(prefix='/mail',tags = ['mailing'])

with open('config.yml', 'r') as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

username = yaml_data['email_creds']['mail']
app_password = yaml_data['email_creds']['app_password']

@router.get("/get_mail_count/")
def read_mails():
    mails = count_emails_received(username, app_password, 2)
    if mails is None:
        raise HTTPException(status_code=404, detail="Customers not found")
    return mails

@router.get("/get_mail_by_senders/")
def read_mails():
    mails = count_unique_senders(username, app_password, 1)
    if mails is None:
        raise HTTPException(status_code=404, detail="Customers not found")
    return mails
