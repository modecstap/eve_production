from typing import Optional, Callable, Type, Any, Sequence

from sqlalchemy import delete, select, Row, RowMapping, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

from src.storage.database import Database
from src.storage.declarative_base import DeclarativeBase
from src.storage.repositories.wrappers import ensure_session


class BaseRepository:
    def __init__(self, entity: Type[DeclarativeBase]):
        self.db = Database()
        self._entity: Type[DeclarativeBase] = entity

    def create_session(self) -> AsyncSession:
        return self.db.async_session_maker()

    @ensure_session
    async def execute_query(
            self,
            query: str,
            params: dict[str: Any],
            session: AsyncSession = None
    ):
        return await session.execute(
            text(query),
            params=params
        )

    @ensure_session
    async def get_entities(
            self,
            filters: Optional[list] = None,
            order_by: Optional[Callable] = None,
            offset: int = 0,
            limit: int = 100,
            session: AsyncSession = None
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        query = select(self._entity)

        if filters:
            query = query.where(*filters)

        if order_by:
            query = query.order_by(order_by)

        query = query.offset(offset)
        query = query.limit(limit)

        result = await session.execute(query)
        return result.scalars().all()

    @ensure_session
    async def get_entity_by_id(self, entity_id: int, session: AsyncSession = None) -> declarative_base:
        result = await session.execute(
            select(self._entity)
            .where(self._entity.id == entity_id)
        )
        return result.scalar_one_or_none()

    @ensure_session
    async def insert(self, entities, session: AsyncSession = None) -> list:
        session.add_all(entities)
        await session.flush()
        await session.commit()
        return entities

    @ensure_session
    async def update(self, transaction_entities, session: AsyncSession = None):
        merged_entities = [await session.merge(transaction_entity) for transaction_entity in transaction_entities]
        session.add_all(merged_entities)
        await session.commit()
        return merged_entities

    @ensure_session
    async def delete(self, ids: list[int], session: AsyncSession = None):

        await session.execute(
            delete(self._entity).where(self._entity.id.in_(ids))
        )
        await session.commit()
