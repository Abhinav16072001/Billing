import os
import httpx
import shutil
import concurrent.futures
from bs4 import BeautifulSoup
import requests
import re

from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Security, status,  UploadFile, Form
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from starlette.responses import FileResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database.security import *
from app.database.actions import *
from app.database.session import get_db
from app.models.token import Token
from app.models.user import User, CreateUserRequest
from app.connections.video import download_youtube_video

router = APIRouter(prefix='/download', tags=['download'])

download_directory = os.path.join(
    os.path.expanduser("~"), "Downloads")

if not os.path.exists(download_directory):
    os.makedirs(download_directory)


@router.post("/video/")
async def download_videos(video_urls: list = Form(...)):
    if not video_urls:
        raise HTTPException(status_code=400, detail="No video URLs provided.")

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(
            download_video, url, download_directory): url for url in video_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            result = future.result()
            results.append(result)

    return {"message": "All videos downloaded.", "results": results}
