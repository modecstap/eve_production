from decimal import Decimal

from sqlalchemy import select

from src.storage.repositories.base import BaseRepository
from src.storage.tables import Station


class StationRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Station

    async def get_station_material_efficiency(self, station_id: int) -> Decimal:
        result = await self._session.execute(
            select(Station.material_efficiency).where(Station.id == station_id)
        )
        return result.scalar_one_or_none()
