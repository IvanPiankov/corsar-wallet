from uuid import UUID

from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.repositories.db_models import users
from models.auth import User, UserInternal
from utils.custom_exception import InternalException
from utils.exceptions.user_exception import NotUniqEmail, NotUniqLogin, UserNotFound


class UserRepository:
    def __init__(self, db: AsyncEngine):
        self._db = db

    @staticmethod
    def _build_user(item: Row) -> User:
        return User(
            user_id=UUID(int=item.user_id.int),
            login=item.login,
            email=item.email,
            wallet_currency=item.wallet_currency if item.wallet_currency else None,
            hashed_password=item.hashed_password,
        )

    @staticmethod
    def _build_internal_user(item: Row) -> User:
        return UserInternal(
            user_id=UUID(int=item.user_id.int),
            login=item.login,
            email=item.email,
            wallet_currency=item.wallet_currency if item.wallet_currency else None,
        )

    async def get_user_by_login(self, login: str) -> User:
        select_query = users.select().where(users.c.login == login)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if item := row.first():
            return self._build_user(item)
        raise UserNotFound

    async def get_user_by_email(self, email: str) -> User:
        select_query = users.select().where(users.c.email == email)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if item := row.first():
            return self._build_user(item)
        raise UserNotFound

    async def check_uniq_login(self, login: str) -> None:
        select_query = users.select().where(users.c.login == login)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if row.first():
            raise NotUniqLogin
        return None

    async def check_uniq_email(self, email: str) -> None:
        select_query = users.select().where(users.c.email == email)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if row.first():
            raise NotUniqEmail
        return None

    async def get_user_by_id(self, user_id: UUID) -> UserInternal:
        select_query = users.select().where(users.c.user_id == user_id)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if item := row.first():
            return self._build_internal_user(item)
        raise UserNotFound

    async def create_user(self, user: User) -> UserInternal:
        insert_query = users.insert().values(user.to_dict()).returning(users)
        async with self._db.connect() as conn:
            row = await conn.execute(insert_query)
            await conn.commit()
        if item := row.first():
            return self._build_internal_user(item)
        raise InternalException
