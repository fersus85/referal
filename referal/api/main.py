from fastapi import FastAPI

from .routers import users, login, codes, referals


app = FastAPI()


app.include_router(login.router)
app.include_router(users.router)
app.include_router(codes.router)
app.include_router(referals.router)
