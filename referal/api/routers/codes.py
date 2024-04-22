from typing import Annotated

from fastapi import APIRouter, Depends
import aioredis

from referal.postgres_db.models import UserReferer
from referal.api.routers.utils import check_ref_code
from referal.core.security import create_referal_code
from referal.api.dependencies import get_current_user, SessionConn
from referal.postgres_db.crud import update_user_referer_code, get_code
from referal.core.config import settings


router = APIRouter(
    prefix="/code",
    tags=["codes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def create_ref_code(db: SessionConn,
                    user: Annotated[UserReferer,
                                    Depends(get_current_user)]) -> str:
    '''
    Создаёт и возвращает реферальный код для зарегестрированного реферера
    '''

    if user.referal_code:
        if check_ref_code(user.referal_code):
            return f'you already have active code: {user.referal_code}'
    code = create_referal_code(user.email)
    update_user_referer_code(db, user, code)
    return f'your new active code: {code}'


@router.delete('/')
def delete_ref_code(db: SessionConn,
                    user: Annotated[UserReferer,
                                    Depends(get_current_user)]) -> str:
    '''Удаляет реферальный код реферера'''
    update_user_referer_code(db, user, None)
    return 'Your referal code has deleted'


@router.get('/get_code')
async def get_code_by_email(db: SessionConn, email: str) -> dict:
    '''Принимает email, кэширует и возвращает реферальный код '''
    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_SERVER}",
        )
    cache_code = await redis.get(email)
    if cache_code is not None:
        return {'code_from_cache': cache_code}
    code = await get_code(db, email)
    await redis.set(email, code, ex=1800)
    return {'code_from_db': code}
