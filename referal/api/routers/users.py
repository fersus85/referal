from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.sql.functions import func

from referal.api.dependencies import (
    SessionConn,
    get_user_by_email,
    get_current_user
    )
from referal.postgres_db.schemas import User, UserCreate, UsersRead
from referal.postgres_db.models import UserReferer
from referal.postgres_db import crud


router = APIRouter(
    prefix='/user',
    tags=['users'],
)


@router.post('/', response_model=User)
def create_user(db: SessionConn, user_in: UserCreate) -> Any:
    user = get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this email already exists in the system.',
        )
    user = crud.create_user(db, user_in)
    return user


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=UsersRead,
)
def read_users(session: SessionConn, skip: int = 0, limit: int = 100) -> Any:
    count = session.execute(
        select(func.count()).select_from(UserReferer)
    ).first()
    statement = select(UserReferer).offset(skip).limit(limit)
    users = [tpl[0] for tpl in session.execute(statement).all()]
    return UsersRead(data=users, count=count[0])
