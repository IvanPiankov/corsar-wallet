import logging
from typing import Annotated

import inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse

from models.auth import UserInternal
from models.category import SubcategoryIn, SubcategoryInternal
from services.subcategories import SubcategoriesService
from services.user_service import get_current_user
from utils.exception import InternalException, WalletHttpException
from utils.exceptions.category_exception import CategoryNotFound, NotUniqCatrgoryName
from utils.status_code_message_mapper import ERROR_EXAMPLE_RESPONSE

subcategories_router = APIRouter(prefix="/subcategory", tags=["Subcategory Router"])


def new_subcategory_service() -> SubcategoriesService:
    return inject.instance(SubcategoriesService)


NewSubcategoriesService = Annotated[SubcategoriesService, Depends(new_subcategory_service)]

# TODO: Сделать нормальную проверку токена, а не использовать постоянно зависимость, чтобы что-то доставать.
CurrentUser = Annotated[UserInternal, Depends(get_current_user)]


@subcategories_router.get(
    "",
    summary="Get subcategories",
    response_model=list[SubcategoryInternal],
    responses={401: ERROR_EXAMPLE_RESPONSE},
    dependencies=[Depends(get_current_user)],
)
async def get_subcategories(service: NewSubcategoriesService):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    subcategories = await service.get_subcategories()
    return jsonable_encoder(subcategories)


@subcategories_router.post(
    "",
    summary="Create subcategory",
    response_model=SubcategoryInternal,
    responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE},
    dependencies=[Depends(get_current_user)],
)
async def create_subcategory(subcategory_in: SubcategoryIn, service: NewSubcategoriesService):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    try:
        subcategory = await service.create_subcategory(subcategory_in)
        return jsonable_encoder(subcategory)
    except NotUniqCatrgoryName as e:
        logging.warning(f"Not unique subcategory name - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)


@subcategories_router.put(
    "/{subcategory_id}",
    summary="Update subcategory",
    response_model=SubcategoryInternal,
    responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE, 500: ERROR_EXAMPLE_RESPONSE},
    dependencies=[Depends(get_current_user)],
)
async def update_user_currency(subcategory_id: int, subcategory_in: SubcategoryIn, service: NewSubcategoriesService):
    """Need header with token: ```Authorization: Bearer {token}```"""
    try:
        update_subcategory = await service.update_subcategory(subcategory_id, subcategory_in)
        return jsonable_encoder(update_subcategory)
    except (NotUniqCatrgoryName, CategoryNotFound) as e:
        logging.warning(f"category error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)
    except InternalException as e:
        logging.warning(f"internal error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)


@subcategories_router.delete(
    "/{subcategory_id}",
    summary="Delete subcategory",
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
async def delete_user(subcategory_id: int, service: NewSubcategoriesService):
    """Need header with token: ```Authorization: Bearer {token}```"""
    try:
        await service.delete_category(subcategory_id)
        return ORJSONResponse({"status": "ok"})
    except InternalException as e:
        logging.warning(f"internal - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)
