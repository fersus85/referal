from uuid import UUID

from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func

from referal.postgres_db.models import UserReferer, UserReferal
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


def get_users(db: Session):
    stmt_count = select(func.count()).select_from(UserReferer)
    count = db.execute(stmt_count).first()

    stmt_users = select(UserReferer)
    users = [tpl[0] for tpl in db.execute(stmt_users).all()]

    return count, users


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


def create_referal(db: Session, referer_email: str, referal_email: str):
    referer: UserReferer = get_user_by_email(db, referer_email)
    try:
        referal = db.scalars(
            insert(UserReferal).returning(UserReferal),
            [
                {
                    'referer_id': referer.id,
                    'email': referal_email,
                    'hashed_password': 'psw',
                    'referer': referer,
                }
            ],
        ).first()
        referer.referals.extend([referal])
        db.add(referal)
        db.commit()
        db.refresh(referal)
        db.refresh(referer)
        return referal
    except Exception:
        return 'Referal with same email already in system'


def get_all_referals(db: Session):
    referals = db.execute(select(UserReferal)).all()
    return referals


def get_refs_by_id(db: Session, id: UUID):
    stmt = select(UserReferer).where(UserReferer.id == id)
    result = db.execute(stmt).first()
    if result:
        referals = result[0].referals
        return referals
    return []


async def get_code(db: Session, email) -> str:
    stmt = (
        select(UserReferer.referal_code)
        .where(UserReferer.email == email)
    )
    result = db.execute(stmt).first()
    if result:
        code = result[0]
        return code
    return 'Invalid email or user dont have valid code'
