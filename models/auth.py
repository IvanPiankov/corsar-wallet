from dataclasses import dataclass
from uuid import UUID

from mashumaro import DataClassDictMixin
from pydantic import BaseModel, EmailStr, Field, validator

from models.enums import Currency


class UserAuthIn(BaseModel):
    login: str = Field(min_length=1, max_length=20)
    email: EmailStr
    password_1: str = Field(min_length=8)
    password_2: str = Field(min_length=8)

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
