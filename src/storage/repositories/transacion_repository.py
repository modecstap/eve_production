from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.repositories.base import BaseRepository
from src.storage.repositories.wrappers import ensure_session
from src.storage.tables import Transaction, TypeInfo


class TransactionRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Transaction

    @ensure_session
    async def get_available_materials(self, session: AsyncSession = None):
        result = await session.execute(
            select(
                Transaction.material_id,
                TypeInfo.name,
                func.sum(Transaction.remains).label("count"),
                func.coalesce(func.sum(Transaction.remains * Transaction.price) / func.nullif(func.sum(Transaction.remains), 0), 0).label("mean_price"),
            )
            .join(TypeInfo)
            .group_by(Transaction.material_id, TypeInfo.name)
        )
        return result.all()
