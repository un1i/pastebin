from fastapi_users.authentication import CookieTransport, JWTStrategy
from fastapi_users.authentication import AuthenticationBackend
from app.config import JWT_SECRET
from fastapi_users import FastAPIUsers
from database.models import User
from app.auth.manager import get_user_manager

cookie_transport = CookieTransport(cookie_name='user_auth', cookie_max_age=3600)

SECRET = JWT_SECRET


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
