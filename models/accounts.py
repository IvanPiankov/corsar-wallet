from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from mashumaro import DataClassDictMixin, pass_through
from pydantic import BaseModel, Field

from models.enums import AccountTypes, Currency


class AccountIn(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    account_type: AccountTypes
    balance: Decimal
    currency: Currency


@dataclass(kw_only=True)
class AccountInternal(DataClassDictMixin):
    account_id: UUID = field(default_factory=uuid4)
    user_id: UUID
    name: str
    account_type: AccountTypes
    balance: Decimal
    currency: Currency
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    class Config:
        serialization_strategy = {
            datetime: {
                "serialize": pass_through,
            }
        }


@dataclass(kw_only=True)
class AccountInternalUpdate(DataClassDictMixin):
    name: str
    account_type: AccountTypes
    balance: Decimal
    currency: Currency
    updated_at: datetime = field(default_factory=datetime.now)

    class Config:
        serialization_strategy = {
            datetime: {
                "serialize": pass_through,
            }
        }


@dataclass(kw_only=True)
class AccountOut(DataClassDictMixin):
    account_id: UUID
    user_id: UUID
    name: str
    account_type: AccountTypes
    balance: Decimal
    currency: Currency
    created_at: datetime

    class Config:
        serialization_strategy = {
            datetime: {
                "deserialize": pass_through,
            }
        }
