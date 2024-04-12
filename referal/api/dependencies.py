from typing import Annotated
from collections.abc import Generator

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from referal.postgres_db.crud import get_user_by_email
from referal.postgres_db.schemas import User, TokenData
from referal.core import security
from referal.core.config import settings
from referal.core.db import engine


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/token')


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionConn = Annotated[Session, Depends(get_db)]
TokenOauth = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(session: SessionConn,
                           token: TokenOauth) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user
