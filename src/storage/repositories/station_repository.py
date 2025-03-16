from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.repositories.base import BaseRepository
from src.storage.repositories.wrappers import ensure_session
from src.storage.tables import Station


class StationRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Station

    @ensure_session
    async def get_station_material_efficiency(self, station_id: int, session: AsyncSession = None) -> Decimal:
        result = await session.execute(
            select(Station.material_efficiency).where(Station.id == station_id)
        )
        return result.scalar_one_or_none()
