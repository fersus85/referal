from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from referal.postgres_db.crud import authenticate_user
from referal.core import config
from referal.core.security import create_access_token
from referal.postgres_db.schemas import Token
from referal.api.dependencies import SessionConn


router = APIRouter(
    prefix='/login',
    tags=['login'],
)


@router.post("/token")
async def login_for_access_token(
    db: SessionConn,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(db,
                             form_data.username,
                             form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
