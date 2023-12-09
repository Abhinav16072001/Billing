from pydantic import BaseModel, ValidationError
from typing import Optional


class User(BaseModel):
    username: str
    name: str | None = None
    role: str
    disabled: Optional[bool] = False


class UserInDB(User):
    hashed_password: str


class CreateUserRequest(BaseModel):
    username: str
    name: str | None = None
    password: str
    role: str


class UserAccessUpdate(BaseModel):
    username: str
    disabled: bool
