from typing import Any, Coroutine, Sequence

from sqlalchemy import func, Row, RowMapping
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.storage.repositories.base import BaseRepository
from src.storage.repositories.wrappers import ensure_session
from src.storage.tables import Transaction, TypeInfo


class TransactionRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Transaction

    @ensure_session
    async def get_entities(
            self,
            *args,
            session: AsyncSession = None,
            replace_id_with_name: bool = False
    ) -> list[Transaction]:
        query = select(Transaction)
        if replace_id_with_name:
            query = query.options(
                joinedload(Transaction.product),
                joinedload(Transaction.material)
            )

        result = await session.execute(query)
        return result.scalars().all()

    @ensure_session
    async def get_transactions_by_type_id(self, type_id: list[int], session: AsyncSession = None) -> list[Transaction]:
        query = (
            select(Transaction)
            .where(Transaction.material_id.in_(type_id))
        )

        result = await session.execute(query)

        return result.scalars().all()

    @ensure_session
    async def get_available_materials(self, type_id: list[int] = None, session: AsyncSession = None):
        query = (
            select(
                Transaction.material_id,
                TypeInfo.name,
                func.sum(Transaction.remains).label("count"),
                func.coalesce(
                    func.sum(Transaction.remains * Transaction.price) / func.nullif(func.sum(Transaction.remains), 0), 0
                ).label("mean_price"),
            )
            .join(TypeInfo)
            .group_by(Transaction.material_id, TypeInfo.name)
        )

        if type_id:
            query = query.where(Transaction.material_id.in_(type_id))

        result = await session.execute(query)

        return result.all()
