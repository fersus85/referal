from fastapi import APIRouter

from referal.postgres_db import crud
from referal.api.routers.utils import check_ref_code
from referal.api.dependencies import SessionConn
from referal.postgres_db.schemas import (
    ReferalRead,
    ReferalsRead,
    ReferalCreate)

router = APIRouter(
    prefix='/referal',
    tags=['referal'],
)


@router.post('/', response_model=ReferalRead | str)
def create_referal(db: SessionConn, payload: ReferalCreate):
    '''Create referal by referer code'''
    referer_email = check_ref_code(payload.code)
    if not referer_email:
        return 'Invalid referal code'

    referal = crud.create_referal(db, referer_email, payload.email)
    return referal


@router.get('/all/', response_model=ReferalsRead)
def get_all_referals(db: SessionConn):
    lst = crud.get_all_referals(db)
    referals = [ref[0] for ref in lst]
    return ReferalsRead(referals=referals)
