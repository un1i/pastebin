from fastapi import FastAPI
from paste.router import router as router_posts
from pages.router import router as router_pages
from auth.auth import auth_backend
from auth.schemas import UserRead, UserCreate
from fastapi_users import FastAPIUsers
from database.models import User
from auth.manager import get_user_manager

app = FastAPI(title='Pastebin')

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(router_posts)

app.include_router(router_pages)

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
