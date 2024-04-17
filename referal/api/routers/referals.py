from fastapi import APIRouter

import referal.postgres_db.crud as crud
from referal.postgres_db.schemas import ReferalRead, ReferalsRead
from referal.api.routers.utils import check_ref_code
from referal.api.dependencies import SessionConn

router = APIRouter(
    prefix='/referal',
    tags=['referal'],
)


@router.post('/', response_model=ReferalRead)
def create_referal(db: SessionConn, code: str, email: str):
    referer_email = check_ref_code(code)
    if not referer_email:
        return 'Invalid referal code'

    referal = crud.create_referal(db, referer_email, email)
    return referal


@router.get('/all/', response_model=ReferalsRead)
def get_all_referals(db: SessionConn):
    referals = [ref[0] for ref in crud.get_all_referals(db)]
    return ReferalsRead(referals=referals)
