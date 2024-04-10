from typing import Annotated

from fastapi import Depends, FastAPI

from .dependencies import get_current_active_user
from .routers import items, login
from ..schemas import User


app = FastAPI()


app.include_router(login.router)
app.include_router(items.router)


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
