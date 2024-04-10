from referal.api.dependencies import get_user
from referal.schemas import User
from referal.core import security


def authenticate_user(fake_db, username: str, password: str) -> User:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user
