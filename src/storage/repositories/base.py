import asyncio
from abc import ABC
from heapq import merge

from sqlalchemy import delete, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.database import Database
from src.storage.repositories.wrappers import ensure_session

class BaseRepository(ABC):
    def __init__(self):
        self.db = Database()

    def create_session(self) -> AsyncSession:
        return self.db.async_session_maker()

    @ensure_session
    async def get_entities(self, session: AsyncSession = None) -> list:
        result = await session.execute(select(self._entity))
        return result.scalars().all()

    @ensure_session
    async def get_entitiy_by_id(self, entity_id: int, session: AsyncSession = None) -> declarative_base:
        result = await session.execute(
            select(self._entity)
            .where(self._entity.id == entity_id)
        )
        return result.scalars().all()

    @ensure_session
    async def insert(self, entities, session: AsyncSession = None) -> list:
        session.add_all(entities)
        await session.flush()
        await session.commit()
        return entities

    @ensure_session
    async def update(self, transaction_entities, session: AsyncSession = None):

        await session.execute(
            merge(transaction_entities)
        )
        await session.commit()

    @ensure_session
    async def delete(self, ids: list[int], session: AsyncSession = None):

        await session.execute(
            delete(self._entity).where(self._entity.id.in_(ids))
        )
        await session.commit()
