from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session

from referal.postgres_db.models import UserReferer
from referal.postgres_db.schemas import UserCreate
from referal.core import security as sec


def get_user_by_email(db: Session, email: str) -> UserReferer | None:
    statement = select(UserReferer).where(UserReferer.email == email)
    user = db.execute(statement).first()
    if user:
        return user[0]
    return None


def authenticate_user(db: Session,
                      username: str,
                      password: str) -> UserReferer:
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not sec.verify_password(password, user.hashed_password):
        return False
    return user


def create_user(db: Session, user_create: UserCreate) -> UserReferer:
    user = db.scalars(
        insert(UserReferer).returning(UserReferer),
        [
            {
                'full_name': user_create.full_name,
                'email': user_create.email,
                'hashed_password': sec.get_password_hash(user_create.password),
                'referal_code': None,
                'referals': []
            }
        ],
    ).first()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_referer_code(db: Session,
                             user: UserReferer,
                             values: str | None) -> None:
    stmt = (
        update(UserReferer)
        .where(UserReferer.email == user.email)
        .values(referal_code=values)
    )
    db.execute(stmt)
    db.commit()
    return
