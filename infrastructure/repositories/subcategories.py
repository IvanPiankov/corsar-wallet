from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.repositories.db_models import subcategory
from models.category import SubcategoryIn, SubcategoryInternal
from utils.exception import InternalException


class SubcategoriesRepository:
    def __init__(self, db: AsyncEngine):
        self._db = db

    @staticmethod
    def _build_subcategories_response(item: Row) -> SubcategoryInternal:
        return SubcategoryInternal(
            subcategory_id=item.subcategory_id, category_id=item.category_id, name=item.name, icon=item.icon
        )

    async def get_subcategories(self) -> list[SubcategoryInternal]:
        select_query = subcategory.select()
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        if items := row.all():
            return [self._build_subcategories_response(item) for item in items]
        return []

    async def check_uniq_subcategory_name(self, name: str, category_id: int) -> bool:
        select_query = subcategory.select().where(subcategory.c.name == name, subcategory.c.category_id == category_id)
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        return bool(row.first())

    async def check_uniq_subcategory_name_with_id(self, name: str, subcategory_id: int) -> bool:
        select_query = subcategory.select().where(
            (subcategory.c.name == name) & (subcategory.c.subcategory_id != subcategory_id)
        )
        async with self._db.connect() as conn:
            row = await conn.execute(select_query)
        return bool(row.first())

    async def create_subcategory(self, subcategory_in: SubcategoryIn) -> SubcategoryInternal:
        insert_query = subcategory.insert().values(subcategory_in.dict()).returning(subcategory)
        async with self._db.connect() as conn:
            row = await conn.execute(insert_query)
            await conn.commit()
        if item := row.first():
            return self._build_subcategories_response(item)
        raise InternalException

    async def update_subcategory(
        self, subcategory_id: int, subcategory_in: SubcategoryIn
    ) -> SubcategoryInternal | None:
        update_query = (
            subcategory.update()
            .values(subcategory_in.dict())
            .where(subcategory.c.subcategory_id == subcategory_id)
            .returning(subcategory)
        )
        async with self._db.connect() as conn:
            row = await conn.execute(update_query)
            await conn.commit()
        if item := row.first():
            return self._build_subcategories_response(item)
        return None

    async def delete_subcategory(self, subcategory_id: int) -> None:
        delete_query = subcategory.delete().where(subcategory.c.category_id == subcategory_id).returning()
        async with self._db.connect() as conn:
            await conn.execute(delete_query)
            await conn.commit()
