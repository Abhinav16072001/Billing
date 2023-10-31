from pydantic import BaseModel, ValidationError


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class CreateUserRequest(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    password: str
