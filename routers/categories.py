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

# TODO: Сделать нормальную проверку токена, а не использовать постоянно зависимость, чтобы что-то доставать.
CurrentUser = Annotated[UserInternal, Depends(get_current_user)]


@categories_router.get(
    "",
    summary="Get categories",
    response_model=list[CategoryInternal],
    responses={401: ERROR_EXAMPLE_RESPONSE},
    dependencies=[Depends(get_current_user)],
)
async def get_categories(service: NewCategoriesService):
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
    dependencies=[Depends(get_current_user)],
)
async def create_category(category_in: CategoryIn, service: NewCategoriesService):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    try:
        category = await service.create_category(category_in)
        return jsonable_encoder(category)
    except NotUniqCatrgoryName as e:
        logging.warning(f"Not unique category name - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)


@categories_router.put(
    "/{category_id}",
    summary="Update category",
    response_model=CategoryInternal,
    responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE, 500: ERROR_EXAMPLE_RESPONSE},
    dependencies=[Depends(get_current_user)],
)
async def update_user_currency(category_id: int, category_in: CategoryIn, service: NewCategoriesService):
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
    dependencies=[Depends(get_current_user)],
)
async def delete_user(category_id: int, service: NewCategoriesService):
    """Need header with token: ```Authorization: Bearer {token}```"""
    try:
        await service.delete_category(category_id)
        return ORJSONResponse({"status": "ok"})
    except InternalException as e:
        logging.warning(f"internal - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)
