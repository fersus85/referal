from typing import Annotated

from fastapi import HTTPException, status, Body
from jose import JWTError, jwt, ExpiredSignatureError

from referal.core.config import settings
from referal.core import security


def check_ref_code(ref_code: Annotated[str, Body()]) -> bool:
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Expires signature or not validate email",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(ref_code, settings.SECRET_KEY,
                             algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError:
        return False
    except JWTError:
        raise credentials_exception
    return True
