from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.paste.router import router as router_posts
from app.pages.router import router as router_pages
from app.profile.router import router as router_profile
import app.exception_handlers as exc_handlers
from app.auth.auth import auth_backend, fastapi_users
from app.auth.schemas import UserRead, UserCreate

exception_handlers = {
    500: exc_handlers.internal_exception_handler,
    503: exc_handlers.unavailable_exception_handler,
    404: exc_handlers.not_found_exception_handler,
    422: exc_handlers.unprocessable_content_handler,
    RequestValidationError: exc_handlers.validate_exception_handler,
}

app = FastAPI(title='Pastebin', exception_handlers=exception_handlers)

app.include_router(router_posts)

app.include_router(router_pages)

app.include_router(router_profile)

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


