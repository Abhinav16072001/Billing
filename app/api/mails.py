import yaml
import datetime
from fastapi import APIRouter, HTTPException, Depends, WebSocket
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.connections.mailing import *
from app.connections.convert import *
from starlette.responses import JSONResponse

router = APIRouter(prefix='/mail', tags=['mailing'])

with open('app/utility/config.yml', 'r') as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)

username = yaml_data['email_creds']['mail']
app_password = yaml_data['email_creds']['app_password']


@router.get("/info/{days}")
def mails_info(days: int):
    info = fetch_email_info(username, app_password, days)
    if info is None:
        raise HTTPException(status_code=404, detail="info not found")
    return info

@router.get("/count/{days}")
def read_mails(days: int):
    mails_count = count_emails_received(username, app_password, days)
    if mails_count is None:
        raise HTTPException(status_code=404, detail="count not found")
    return mails_count

@router.get("/senders/{days}")
def read_mails(days: int):
    senders = unique_senders_count(username, app_password, days)
    if senders is None:
        raise HTTPException(status_code=404, detail="senders not found")
    return senders

@router.get("/senders/{days}/download")
def download_senders(days: int):
    senders = unique_senders_count(username, app_password, days)
    if senders is None:
        raise HTTPException(status_code=404, detail="Senders not found")
    current_date = datetime.now()
    date = current_date.strftime('%c').split()[:3]
    filename = f"senders_{'_'.join(date)}"

    convert_to_csv(filename, senders)
    response = JSONResponse(content=senders)
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}.csv"'

    return response

@router.get("/info/{days}/download")
def download_count(days: int):
    info = fetch_email_info(username, app_password, days)
    if info is None:
        raise HTTPException(status_code=404, detail="info not found")
    current_date = datetime.now()
    date = current_date.strftime('%c').split()[:3]
    filename = f"email_info_{'_'.join(date)}"

    convert_to_csv(filename, info)
    response = JSONResponse(content=info)
    response.headers["Content-Disposition"] = f'attachment; filename={filename}.csv"'
    
    return response
