import inject
from fastapi import APIRouter, Body, Depends
from fastapi.responses import ORJSONResponse

from models.auth import UserInternal
from models.enums import Currency
from services.user_service import UserService, get_current_user

user_router = APIRouter(prefix="/user", tags=["User Router"])


def new_user_service() -> UserService:
    return inject.instance(UserService)


@user_router.get(
    "",
    summary="Get users",
    response_model=UserInternal,
    description="Need header with token: ```Authorization: Bearer {token}```",
)
async def get_user(current_user: UserInternal = Depends(get_current_user)):
    return ORJSONResponse(current_user.to_dict())


@user_router.put(
    "",
    summary="Update user currency",
    response_model=UserInternal,
    description="Need header with token: ```Authorization: Bearer {token}```",
)
async def update_user_currency(
    current_user: UserInternal = Depends(get_current_user),
    wallet_currency: Currency = Body(
        ..., embed=True, title="Currency", description="Now work only this currency: `USD`, `RUB`, `EUR`"
    ),
    service: UserService = Depends(new_user_service),
):
    update_user_data = await service.update_user_currency(current_user, wallet_currency)
    return ORJSONResponse(update_user_data.to_dict())


@user_router.delete(
    "",
    summary="Delete current user",
    response_model=None,
    description="Need header with token: ```Authorization: Bearer {token}```",
)
async def delete_user(
    current_user: UserInternal = Depends(get_current_user), service: UserService = Depends(new_user_service)
):
    await service.delete_user(current_user.user_id)
    return ORJSONResponse({"status": "ok"})
