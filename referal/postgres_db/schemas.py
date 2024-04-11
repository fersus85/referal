from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool | None = None


class UserCreate(User):
    password: str


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ReferalCode(BaseModel):
    code: str
    expire: datetime
    active: bool
