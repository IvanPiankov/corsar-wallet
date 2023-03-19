import inject
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from models.auth import Tokens, UserAuthIn, UserInternal
from services.auth_service import AuthService, get_current_user

auth_router = APIRouter(tags=["Auth User Route"])


def new_auth_service() -> AuthService:
    return inject.instance(AuthService)


@auth_router.post("/sign-up", summary="Create new user", response_model=UserInternal)
async def sign_up(user_auth_in: UserAuthIn, service: AuthService = Depends(new_auth_service)):
    user_out = await service.sign_up(user_auth_in)
    return ORJSONResponse(user_out.to_dict())


@auth_router.post("/login", summary="Login user", response_model=Tokens)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(new_auth_service)):
    tokens = await service.login(form_data.username, form_data.password)
    return ORJSONResponse(tokens.to_dict())


@auth_router.get("/get-me", summary="Get current user", response_model=UserInternal)
async def login(current_user: UserInternal = Depends(get_current_user)):
    return ORJSONResponse(current_user.to_dict())
