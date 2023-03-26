import asyncio
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from jose import jwt
from passlib.context import CryptContext

from infrastructure.repositories.users_repository import UserRepository
from models.auth import Tokens, User, UserAuthIn, UserInternal
from settings import Settings
from utils.exceptions.user_exception import InvalidPassword, NotUniqEmail, NotUniqLogin

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


class AuthService:
    def __init__(self, users_repo: UserRepository) -> None:
        self._users_repo = users_repo

    async def get_user_by_id(self, user_id: UUID) -> UserInternal:
        return await self._users_repo.get_user_by_id(user_id)

    @staticmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)

    @staticmethod
    async def create_access_token(subject: UUID, token_expires_time: int) -> str:
        expires_delta = datetime.utcnow() + timedelta(seconds=token_expires_time)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, Settings.JWT_SECRET_KEY, Settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def create_refresh_token(subject: UUID, token_expires_time: int) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=token_expires_time)

        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, Settings.JWT_REFRESH_SECRET_KEY, Settings.ALGORITHM)
        return encoded_jwt

    async def sign_up(self, user_auth: UserAuthIn) -> UserInternal:
        check_uniq_login_email = asyncio.gather(
            self._users_repo.check_uniq_login(user_auth.login), self._users_repo.check_uniq_email(user_auth.email)
        )
        try:
            await check_uniq_login_email
        except (NotUniqLogin, NotUniqEmail) as e:
            check_uniq_login_email.cancel()
            raise e
        user = User(
            user_id=uuid4(),
            login=user_auth.login,
            email=user_auth.email,
            hashed_password=get_hashed_password(user_auth.password_1),
        )
        user_from_db = await self._users_repo.create_user(user)
        return UserInternal.from_dict(user_from_db.to_dict())

    async def login(self, username: str, password: str) -> Tokens:
        user = await self._users_repo.get_user_by_login(username)
        if not self.verify_password(password, user.hashed_password):
            raise InvalidPassword
        else:
            access_token, refresh_token = await asyncio.gather(
                self.create_access_token(user.user_id, Settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                self.create_refresh_token(user.user_id, Settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            )
        return Tokens(access_token, refresh_token)
