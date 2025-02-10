from sqlalchemy import select

from src.storage.repositories.base import BaseRepository
from src.storage.tables import MaterialList


class MaterialListRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = MaterialList

    async def get_materials_by_type_id(self, type_id: int) -> list[MaterialList]:
        async with self.db.async_session() as session:
            products = await session.execute(
                select(
                    MaterialList
                ).where(
                    MaterialList.type_id == type_id
                )
            )
            return products.scalars().all()
