from uuid import UUID

import jwt
from jose import JWTError

from settings import Settings
from utils.exceptions.user_exception import UserNotFound


def parse_jwt(token: str) -> UUID:
    try:
        payload = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithms=[Settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise UserNotFound
        user_id = UUID(user_id)
        return user_id
    except JWTError as e:
        raise e
