from uuid import UUID

from infrastructure.repositories.accounts import AccountsRepository
from models.accounts import AccountIn, AccountInternal, AccountInternalUpdate, AccountOut


class AccountsService:
    def __init__(self, account_repo: AccountsRepository) -> None:
        self._account_repo = account_repo

    async def get_user_accounts(self, user_id: UUID) -> list[AccountOut]:
        internal_accounts = await self._account_repo.get_user_accounts(user_id)
        return [AccountOut.from_dict(account_internal.to_dict()) for account_internal in internal_accounts]

    async def get_account_by_id(self, user_id: UUID, account_id: UUID) -> AccountOut:
        internal_account = await self._account_repo.get_account_by_id(user_id, account_id)
        return AccountOut.from_dict(internal_account.to_dict())

    async def create_account(self, user_id: UUID, account_in: AccountIn) -> AccountOut:
        internal_account = AccountInternal.from_dict(account_in.dict() | {"user_id": str(user_id)})
        if await self._account_repo.check_uniq_user_account_name(internal_account.user_id, internal_account.name):
            # TODO: Change error
            raise ValueError
        new_account = await self._account_repo.create_account(internal_account)
        return AccountOut.from_dict(new_account.to_dict())

    async def update_user_account(self, user_id: UUID, account_id: UUID, account_in: AccountIn) -> AccountOut:
        print(account_in.dict())
        internal_account = AccountInternalUpdate.from_dict(account_in.dict())
        updated_account = await self._account_repo.update_user_account(user_id, account_id, internal_account)
        return AccountOut.from_dict(updated_account.to_dict())

    async def delete_user_account(self, account_id: UUID) -> None:
        return await self._account_repo.delete_user_account(account_id)
