from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.repositories.base import BaseRepository
from src.storage.repositories.wrappers import ensure_session
from src.storage.tables import MaterialList


class MaterialListRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = MaterialList

    @ensure_session
    async def get_materials_by_type_id(self, type_id: int, session: AsyncSession = None) -> list[MaterialList]:
        products = await session.execute(
            select(
                MaterialList
            ).where(
                MaterialList.type_id == type_id
            )
        )
        return products.scalars().all()
