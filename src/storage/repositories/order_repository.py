from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.server.handlers.models import StatusModel
from src.storage.repositories.base import BaseRepository
from src.storage.repositories.wrappers import ensure_session
from src.storage.tables import Order


class OrderRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Order

    @ensure_session
    async def update_statuses(self, statuses: list[StatusModel], session: AsyncSession = None):
        for status in statuses:
            await session.execute(
                update(Order)
                .where(Order.id == status.order_id)
                .values(status=status.status)
            )
        await session.commit()
