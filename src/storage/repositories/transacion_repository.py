from sqlalchemy import func
from sqlalchemy import select

from src.storage.repositories.base import BaseRepository
from src.storage.tables import Transaction, Material


class TransactionRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Transaction

    async def get_available_materials(self):
        result = await self._session.execute(
            select(
                Transaction.material_id,
                Material.name,
                func.sum(Transaction.remains).label("count"),
                func.coalesce(func.sum(Transaction.remains * Transaction.price) / func.nullif(func.sum(Transaction.remains), 0), 0)
            )
            .join(Material)
            .group_by(Transaction.material_id, Material.name)
        )
        return result.all()
