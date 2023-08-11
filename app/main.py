from fastapi import FastAPI
from paste.router import router as router_posts
from pages.router import router as router_pages
from auth.auth import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

app = FastAPI(title='Pastebin')

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
