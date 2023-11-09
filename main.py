from fastapi import FastAPI
from app.api import mails, auth, user, download, admin

app = FastAPI()

app.include_router(mails.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(download.router)
app.include_router(admin.router)
