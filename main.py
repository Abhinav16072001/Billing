from fastapi import FastAPI
from app.api import mails, auth, user

app = FastAPI()

app.include_router(mails.router)
app.include_router(auth.router)
app.include_router(user.router)
