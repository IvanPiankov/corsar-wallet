from infrastructure.repositories.subcategories import SubcategoriesRepository
from models.category import SubcategoryIn, SubcategoryInternal
from utils.exceptions.category_exception import CategoryNotFound, NotUniqCatrgoryName


class SubcategoriesService:
    def __init__(self, subcategory_repo: SubcategoriesRepository) -> None:
        self._subcategory_repo = subcategory_repo

    async def get_subcategories(self) -> list[SubcategoryInternal]:
        return await self._subcategory_repo.get_subcategories()

    async def create_subcategory(self, subcategory_in: SubcategoryIn) -> SubcategoryInternal:
        if await self._subcategory_repo.check_uniq_subcategory_name(subcategory_in.name, subcategory_in.category_id):
            raise NotUniqCatrgoryName
        return await self._subcategory_repo.create_subcategory(subcategory_in)

    async def update_subcategory(self, subcategory_id: int, subcategory_in: SubcategoryIn) -> SubcategoryInternal:
        # TODO: Сделать так, чтобы можно было проверять по категории
        if await self._subcategory_repo.check_uniq_subcategory_name_with_id(subcategory_in.name, subcategory_id):
            raise NotUniqCatrgoryName

        if updated_subcategory := await self._subcategory_repo.update_subcategory(subcategory_id, subcategory_in):
            return updated_subcategory
        else:
            raise CategoryNotFound

    async def delete_category(self, subcategory_id: int) -> None:
        return await self._subcategory_repo.delete_subcategory(subcategory_id)
