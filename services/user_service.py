import logging
from typing import Annotated
from uuid import UUID

import inject
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from infrastructure.repositories.users import UserRepository
from models.auth import UserInternal
from models.enums import Currency
from settings import Settings
from utils.exception import WalletHttpException
from utils.exceptions.user_exception import UserNotFound
from utils.jwt_parser import parse_jwt

oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="JWT")


class UserService:
    def __init__(self, users_repo: UserRepository) -> None:
        self._users_repo = users_repo

    async def get_user_by_id(self, user_id: UUID) -> UserInternal:
        return await self._users_repo.get_user_by_id(user_id)

    async def delete_user(self, user_id: UUID) -> None:
        return await self._users_repo.delete_user(user_id)

    async def update_user_currency(self, user: UserInternal, wallet_currency: Currency) -> UserInternal:
        return await self._users_repo.update_user_currency(user.user_id, wallet_currency)


async def get_current_user(token: str = Depends(oauth_schema)) -> UserInternal:
    try:
        user_id = parse_jwt(token)
        return await inject.instance(UserService).get_user_by_id(user_id)
    except UserNotFound as e:
        logging.warning(f"Token User Not Found - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=401)
