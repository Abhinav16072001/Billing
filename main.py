from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import mails, auth, user, download, admin, gateway

app = FastAPI()

app.include_router(mails.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(download.router)
app.include_router(admin.router)
app.include_router(gateway.router)


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
