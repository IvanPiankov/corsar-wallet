from dataclasses import dataclass
from uuid import UUID

from mashumaro import DataClassDictMixin
from pydantic import BaseModel, EmailStr, validator

from models.enums import Currency


class UserAuthIn(BaseModel):
    # TODO: Create validator for filed
    login: str
    email: EmailStr
    password_1: str
    password_2: str

    @validator("password_2")
    def passwords_match(cls, v, values, **kwargs):
        if "password_1" in values and v != values["password_1"]:
            raise ValueError("Passwords do not match")
        return v


@dataclass(kw_only=True)
class UserInternal(DataClassDictMixin):
    user_id: UUID
    login: str
    email: str
    wallet_currency: str = Currency.USD


@dataclass(kw_only=True)
class User(UserInternal):
    hashed_password: str


@dataclass
class Tokens(DataClassDictMixin):
    access_token: str
    refresh_token: str
