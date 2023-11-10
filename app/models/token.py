from pydantic import BaseModel, ValidationError


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class SignupToken(BaseModel):
    username: str
    password: str
    role: str


class LoginToken(BaseModel):
    username: str
    password: str
    role: str
