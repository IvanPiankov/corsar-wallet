from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.repositories.db_models import category
from models.category import CategoryIn, CategoryInternal
from utils.exception import InternalException


class CategoriesRepository:
    def __init__(self, db: AsyncEngine):
        self._db = db

    @staticmethod
    def _build_category_response(item: Row) -> CategoryInternal:
        return CategoryInternal(category_id=item.category_id, name=item.name, icon=item.icon)

    async def get_categories(self) -> list[CategoryInternal]:
        select_query = category.select()
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if items := row.all():
            return [self._build_category_response(item) for item in items]
        return []

    async def check_uniq_category_name(self, name: str) -> bool:
        select_query = category.select().where(category.c.name == name)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        return bool(row.first())

    async def check_uniq_category_name_with_id(self, name: str, category_id: int) -> bool:
        select_query = category.select().where((category.c.name == name) & (category.c.category_id != category_id))
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        return bool(row.first())

    async def create_category(self, category_in: CategoryIn) -> CategoryInternal:
        insert_query = category.insert().values(category_in.dict()).returning(category)
        async with self._db.connect() as conn:
            row = await conn.execute(insert_query)
            await conn.commit()
        if item := row.first():
            return self._build_category_response(item)
        raise InternalException

    async def update_category(self, category_id: int, category_in: CategoryIn) -> CategoryInternal | None:
        update_query = (
            category.update()
            .values(category_in.dict())
            .where(category.c.category_id == category_id)
            .returning(category)
        )
        async with self._db.connect() as conn:
            row = await conn.execute(update_query)
            await conn.commit()
        if item := row.first():
            return self._build_category_response(item)
        return None

    async def delete_category(self, category_id: int) -> None:
        delete_query = category.delete().where(category.c.category_id == category_id).returning()
        async with self._db.connect() as conn:
            await conn.execute(delete_query)
            await conn.commit()
