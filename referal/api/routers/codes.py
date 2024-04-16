from typing import Annotated

from fastapi import APIRouter, Depends

from referal.api.routers.utils import check_ref_code
from referal.core.security import create_referal_code
from referal.postgres_db.models import UserReferer
from referal.api.dependencies import get_current_user, SessionConn
from referal.postgres_db.crud import update_user_referer_code


router = APIRouter(
    prefix="/code",
    tags=["codes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def create_ref_code(db: SessionConn,
                    user: Annotated[UserReferer, Depends(get_current_user)]):
    if user.referal_code:
        if check_ref_code(user.referal_code):
            return f'you already have active code: {user.referal_code}'
    code = create_referal_code(user.email)
    update_user_referer_code(db, user, code)
    return f'your new active code: {code}'


@router.delete('/')
def delete_ref_code(db: SessionConn,
                    user: Annotated[UserReferer, Depends(get_current_user)]):
    update_user_referer_code(db, user, None)
    return 'Your referal code has deleted'
