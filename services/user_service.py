from uuid import UUID

import inject
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from infrastructure.repositories.users_repository import UserRepository
from models.auth import UserInternal
from models.enums import Currency
from settings import Settings
from utils.exceptions.user_exception import UserNotFound

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
        payload = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithms=[Settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise UserNotFound
        user_id = UUID(user_id)
    except JWTError as e:
        raise e
    return await inject.instance(UserService).get_user_by_id(user_id)
