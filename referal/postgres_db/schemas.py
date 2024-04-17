from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    email: str
    full_name: str | None = None

    class Config:
        from_attributes = True


class UserCreate(User):
    password: str


class UserRead(User):
    referal_code: str | None


class UsersRead(BaseModel):
    data: list[UserRead]
    count: int


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ReferalRead(BaseModel):
    id: UUID
    referer_id: UUID
    email: str
    referer: User

    class Config:
        from_attributes = True


class ReferalsRead(BaseModel):
    referals: list[ReferalRead]
