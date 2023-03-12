from dataclasses import field
from uuid import UUID, uuid4

from mashumaro import DataClassDictMixin
from pydantic import BaseModel, EmailStr, validator
from pydantic.dataclasses import dataclass


class UserAuthIn(BaseModel):
    # TODO: Create validator for filed
    login: str
    email: EmailStr
    password_1: str
    password_2: str

    @validator('password_2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password_1' in values and v != values['password_1']:
            raise ValueError('Passwords do not match')
        return v


@dataclass
class UserOut(DataClassDictMixin):
    user_id: UUID
    login: str
    email: str
    # TODO: Create wallet_currency if none
    wallet_currency: str | None


@dataclass
class User(UserOut):
    hashed_password: str


@dataclass
class Tokens(DataClassDictMixin):
    access_token: str
    refresh_token: str
