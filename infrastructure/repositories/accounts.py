from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.repositories.db_models import accounts
from models.accounts import AccountInternal, AccountInternalUpdate
from models.enums import AccountTypes, Currency
from utils.exception import InternalException
from utils.exceptions.user_exception import UserNotFound


class AccountsRepository:
    def __init__(self, db: AsyncEngine):
        self._db = db

    @staticmethod
    def _build_account(item: Row) -> AccountInternal:
        return AccountInternal(
            account_id=UUID(int=item.account_id.int),
            user_id=UUID(int=item.user_id.int),
            name=item.name,
            account_type=AccountTypes(item.account_type),
            balance=Decimal(item.balance),
            currency=Currency(item.currency),
            created_at=item.created_at,
            updated_at=item.updated_at,
        )

    async def check_uniq_user_account_name(self, user_id: UUID, name: str) -> bool:
        select_query = accounts.select().where((accounts.c.user_id == user_id) & (accounts.c.name == name))
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        return bool(row.first())

    async def get_user_accounts(self, user_id: UUID) -> list[AccountInternal]:
        select_query = accounts.select().where(accounts.c.user_id == user_id)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if items := row.all():
            return [self._build_account(item) for item in items]
        return []

    async def get_account_by_id(self, user_id: UUID, account_id: UUID) -> AccountInternal:
        select_query = accounts.select().where((accounts.c.user_id == user_id) & (accounts.c.account_id == account_id))
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if item := row.first():
            return self._build_account(item)
        # TODO: create extansion
        raise UserNotFound

    async def create_account(self, account: AccountInternal) -> AccountInternal:
        insert_query = accounts.insert().values(account.to_dict()).returning(accounts)
        async with self._db.connect() as conn:
            row = await conn.execute(insert_query)
            await conn.commit()
        if item := row.first():
            return self._build_account(item)
        raise InternalException

    async def update_user_account(
        self, user_id: UUID, account_id: UUID, update_value: AccountInternalUpdate
    ) -> AccountInternal:
        update_query = (
            accounts.update()
            .values(update_value.to_dict())
            .where((accounts.c.user_id == user_id) & (accounts.c.account_id == account_id))
            .returning(accounts)
        )
        async with self._db.connect() as conn:
            row = await conn.execute(update_query)
            await conn.commit()
        if item := row.first():
            return self._build_account(item)
        raise InternalException

    async def delete_user_account(self, account_id: UUID) -> None:
        delete_query = accounts.delete().where(accounts.c.account_id == account_id)
        async with self._db.connect() as conn:
            await conn.execute(delete_query)
            await conn.commit()
