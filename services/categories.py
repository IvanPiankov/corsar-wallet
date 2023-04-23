from infrastructure.repositories.categories import CategoriesRepository
from models.category import CategoryIn, CategoryInternal
from utils.exceptions.category_exception import CategoryNotFound, NotUniqCatrgoryName


class CategoriesService:
    def __init__(self, category_repo: CategoriesRepository) -> None:
        self._category_repo = category_repo

    async def get_categories(self) -> list[CategoryInternal]:
        return await self._category_repo.get_categories()

    async def create_category(self, category_in: CategoryIn) -> CategoryInternal:
        if await self._category_repo.check_uniq_category_name(category_in.name):
            raise NotUniqCatrgoryName
        return await self._category_repo.create_category(category_in)

    async def update_category(self, category_id: int, category_in: CategoryIn) -> CategoryInternal:
        if await self._category_repo.check_uniq_category_name_with_id(category_in.name, category_id):
            raise NotUniqCatrgoryName

        if updated_category := await self._category_repo.update_category(category_id, category_in):
            return updated_category
        else:
            raise CategoryNotFound

    async def delete_category(self, category_id: int) -> None:
        return await self._category_repo.delete_category(category_id)
