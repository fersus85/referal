from typing import Any, Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from referal.api.dependencies import (
    SessionConn,
    get_user_by_email,
    get_current_user
    )
from referal.postgres_db.schemas import (
    User,
    UserCreate,
    UsersRead,
    ReferalsRead)
from referal.postgres_db.models import UserReferer
from referal.postgres_db import crud
from referal.utils import generate_referal_code_email, send_email


router = APIRouter(
    prefix='/user',
    tags=['users'],
)


@router.post('/', response_model=User)
def create_user(db: SessionConn, user_in: UserCreate) -> Any:
    '''Принимает email, имя и пароль. Создаёт и возвращает Реферера.'''
    user = get_user_by_email(db, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this email already exists in the system.',
        )
    user = crud.create_user(db, user_in)
    return user


@router.get("/",
            dependencies=[Depends(get_current_user)],
            response_model=UsersRead)
def get_all_users(db: SessionConn) -> Any:
    '''Возвращает зарегестрированному рефереру список всех рефереров'''
    count, users = crud.get_users(db)
    return UsersRead(data=users, count=count[0])


@router.get('/getrefs/{ref_id}', response_model=ReferalsRead | str)
def get_referals_by_id_referer(db: SessionConn,
                               ref_id: UUID) -> ReferalsRead | str:
    '''
    В параметре пути принимает id реферера, возвращает список его рефералов
    '''
    referals = crud.get_refs_by_id(db, ref_id)
    if not referals:
        return 'Referals list empty or Invalid ID'
    return ReferalsRead(referals=referals)


@router.get('/email/', response_model=str)
def send_ref_code_by_email(referer: Annotated[
                           UserReferer, Depends(get_current_user)]) -> str:
    '''
    Отправляет зарегестрированному рефереру email с его реферальным кодом
    '''

    email_data = generate_referal_code_email(username=referer.full_name,
                                             code=referer.referal_code)
    try:
        send_email(
            email_to=referer.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    except Exception as ex:
        return ex
    return 'Success sending'
