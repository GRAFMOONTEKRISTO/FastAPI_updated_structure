from fastapi import FastAPI
from fastapi.params import Depends
from fastapi_users import FastAPIUsers

from src.auth.base_config import auth_backend, fastapi_users
from src.database import User
from src.auth.manage import get_user_manager
from src.auth.schemas import UserRead, UserCreate

app = FastAPI(
    title='Trading App'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


current_user = fastapi_users.current_user()


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
