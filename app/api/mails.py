import yaml
from fastapi import APIRouter, HTTPException, Depends, WebSocket
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.customer import Customer, CustomerCreate, CustomerBase
from app.database.actions import create_customer_record, get_customers
from app.connections.mailing import *
from app.connections.convert import *
from starlette.responses import JSONResponse

router = APIRouter(prefix='/mail', tags=['mailing'])

with open('config.yml', 'r') as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

username = yaml_data['email_creds']['mail']
app_password = yaml_data['email_creds']['app_password']


@router.get("/info/{days}")
def mails_info(days: int):
    info = fetch_email_info(username, app_password, days)
    if info is None:
        raise HTTPException(status_code=404, detail="info not found")
    file_name = convert_to_excel("Email_info",info)
    return file_name

@router.get("/count/{days}")
def read_mails(days: int):
    mails = count_emails_received(username, app_password, days)
    if mails is None:
        raise HTTPException(status_code=404, detail="count not found")
    return mails

@router.get("/senders/{days}")
def read_mails(days: int):
    senders = unique_senders_count(username, app_password, days)
    if senders is None:
        raise HTTPException(status_code=404, detail="senders not found")
    file_name = convert_to_excel("Unique_senders_count_info", senders)
    return senders
