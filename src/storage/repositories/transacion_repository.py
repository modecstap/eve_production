from sqlalchemy import func
from sqlalchemy import select

from src.storage.repositories.base import BaseRepository
from src.storage.tables import Transaction, Material


class TransactionRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Transaction

    async def get_available_materials(self):
        async with self.db.async_session() as session:
            result = await session.execute(
                select(
                    Transaction.material_id,
                    Material.name,
                    func.sum(Transaction.remains).label("count"),
                    (func.sum(Transaction.remains * Transaction.price) / func.sum(Transaction.remains)).label(
                        "mean_price")
                )
                .join(Material)
                .group_by(Transaction.material_id, Material.name)
            )
            return result.all()
