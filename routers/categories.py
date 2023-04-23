import logging
from typing import Annotated

import inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse

from models.auth import UserInternal
from models.category import CategoryIn, CategoryInternal
from services.categories import CategoriesService
from services.user_service import get_current_user
from utils.exception import InternalException, WalletHttpException
from utils.exceptions.category_exception import CategoryNotFound, NotUniqCatrgoryName
from utils.status_code_message_mapper import ERROR_EXAMPLE_RESPONSE

categories_router = APIRouter(prefix="/category", tags=["Category Router"])


def new_category_service() -> CategoriesService:
    return inject.instance(CategoriesService)


NewCategoriesService = Annotated[CategoriesService, Depends(new_category_service)]
CurrentUser = Annotated[UserInternal, Depends(get_current_user)]


@categories_router.get(
    "", summary="Get categories", response_model=list[CategoryInternal], responses={401: ERROR_EXAMPLE_RESPONSE}
)
async def get_categories(current_user: CurrentUser, service: NewCategoriesService):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    categories = await service.get_categories()
    return jsonable_encoder(categories)


@categories_router.post(
    "",
    summary="Create category",
    response_model=CategoryInternal,
    responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE},
)
async def create_user_wallet(category_in: CategoryIn, current_user: CurrentUser, service: NewCategoriesService):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    try:
        user_account = await service.create_category(category_in)
        return jsonable_encoder(user_account)
    except NotUniqCatrgoryName as e:
        logging.warning(f"Not unique category name - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)


# @accounts_router.get(
#     "/{account_id}",
#     summary="Get category",
#     response_model=CategoryInternal,
#     responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE},
# )
# async def get_user_account(account_id: UUID, current_user: CurrentUser, service: NewCategoriesService):
#     """
#     Need header with token: ```Authorization: Bearer {token}```
#     """
#     try:
#         user_account = await service.get_account_by_id(current_user.user_id, account_id)
#         return jsonable_encoder(user_account)
#     except AccountNotFound as e:
#         logging.warning(f"account error - {e.error_type}")
#         raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)


@categories_router.put(
    "/{category_id}",
    summary="Update category",
    response_model=CategoryInternal,
    responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE, 500: ERROR_EXAMPLE_RESPONSE},
)
async def update_user_currency(
    category_id: int, category_in: CategoryIn, current_user: CurrentUser, service: NewCategoriesService
):
    """Need header with token: ```Authorization: Bearer {token}```"""
    try:
        update_category = await service.update_category(category_id, category_in)
        return jsonable_encoder(update_category)
    except (NotUniqCatrgoryName, CategoryNotFound) as e:
        logging.warning(f"category error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)
    except InternalException as e:
        logging.warning(f"internal error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)


@categories_router.delete(
    "/{category_id}",
    summary="Delete category",
    response_model=None,
    responses={
        200: {
            "content": {"application/json": {"example": {"status": "ok"}}},
        },
        401: ERROR_EXAMPLE_RESPONSE,
        500: ERROR_EXAMPLE_RESPONSE,
    },
)
async def delete_user(category_id: int, current_user: CurrentUser, service: NewCategoriesService):
    """Need header with token: ```Authorization: Bearer {token}```"""
    try:
        await service.delete_category(category_id)
        return ORJSONResponse({"status": "ok"})
    except InternalException as e:
        logging.warning(f"internal - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)
