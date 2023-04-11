import logging
from typing import Annotated

import inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from models.auth import Tokens, UserAuthIn, UserInternal
from services.auth_service import AuthService
from utils.exception import WalletHttpException
from utils.exceptions.user_exception import InvalidPassword, NotUniqEmail, NotUniqLogin, UserNotFound
from utils.status_code_message_mapper import ERROR_EXAMPLE_RESPONSE

auth_router = APIRouter(prefix="/auth", tags=["Auth User Route"])


def new_user_service() -> AuthService:
    return inject.instance(AuthService)


@auth_router.post(
    "/sign-up",
    summary="Create new user",
    response_model=UserInternal,
    status_code=201,
    responses={404: ERROR_EXAMPLE_RESPONSE},
)
async def sign_up(user_auth_in: UserAuthIn, service: Annotated[AuthService, Depends(new_user_service)]):
    try:
        user_out = await service.sign_up(user_auth_in)
        return jsonable_encoder(user_out)
    except (NotUniqLogin, NotUniqEmail) as e:
        logging.warning(f"sign-in error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)


@auth_router.post(
    "/login",
    summary="Login user",
    response_model=Tokens,
    responses={404: ERROR_EXAMPLE_RESPONSE},
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(new_user_service)):
    try:
        tokens = await service.login(form_data.username, form_data.password)
        return jsonable_encoder(tokens)
    except (UserNotFound, InvalidPassword) as e:
        logging.warning(f"login error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)
