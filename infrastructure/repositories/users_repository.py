from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.repositories.db_models import users
from models.auth import User

from sqlalchemy.engine import Row


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
            hashed_password=item.hashed_password
        )

    async def get_user_by_login(self, login: str) -> User:
        select_query = users.select().where(users.c.login == login)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if item := row.first():
            return self._build_user(item)
        # TODO: Придумать ошибку
        raise ValueError

    async def get_user_by_email(self, email: str) -> User:
        select_query = users.select().where(users.c.email == email)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if item := row.first():
            return self._build_user(item)
        # TODO: Придумать ошибку
        raise ValueError

    async def check_uniq_email_login(self, email: str, login: str) -> None:
        select_query = users.select().where((users.c.email == email) & (users.c.login == login))
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if item := row.first():
            # TODO: Переделать чтобы проверяли юзера
            raise ValueError
        return None

    async def get_user_by_id(self, user_id: UUID) -> User:
        select_query = users.select().where(users.c.user_id == user_id)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if item := row.first():
            return self._build_user(item)
        # TODO: Придумать ошибку
        raise ValueError

    async def create_user(self, user: User) -> User:
        insert_query = users.insert().values(user.to_dict()).returning(users)
        async with self._db.connect() as conn:
            row = await conn.execute(insert_query)
            await conn.commit()
        if item := row.first():
            return self._build_user(item)
        raise ValueError
