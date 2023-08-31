from typing import Optional, Union
import re

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.exceptions import InvalidPasswordException

from database.database import get_user_db
from database.models import User
from app.config import MANAGER_AUTH
from app.auth import schemas

SECRET = MANAGER_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def validate_password(
        self, password: str, user: Union[schemas.UserCreate, User]
    ) -> None:
        pattern = r'^[a-zA-z0-9@_%-]+$'
        if len(password) < 8 or not re.fullmatch(pattern, password):
            raise InvalidPasswordException('invalid password')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
