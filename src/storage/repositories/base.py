from abc import ABC
from heapq import merge

from sqlalchemy import delete, select
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

from src.storage.database import Database


class BaseRepository(ABC):
    def __init__(self):
        self.db = Database()
        self._entity: declarative_base = None

        self._session: AsyncSession = self.db.async_session_maker()

    async def start_transaction(self):
        if self._session.is_active:
            return

        await self._session.begin()

    async def commit_transaction(self):
        if self._session.is_active:
            await self._session.commit()

    async def rollback_transaction(self):
        if self._session.is_active:
            await self._session.rollback()

    async def close_transaction(self):
        if self._session.is_active:
            await self._session.close()

    async def get_entities(self) -> list[declarative_base]:
        
        result = await self._session.execute(
            select(self._entity)
        )
        return result.scalars().all()

    async def get_entitiy_by_id(self, entity_id: int) -> declarative_base:
        
        result = await self._session.execute(
            select(self._entity)
            .where(self._entity.id == entity_id)
        )
        return result.scalars().all()

    async def insert(self, entities) -> list:
        
        self._session.add_all(entities)
        await self._session.flush()
        await self._session.commit()
        return entities

    async def update(self, transaction_entities):
        
        await self._session.execute(
            merge(transaction_entities)
        )
        await self._session.commit()

    async def delete(self, ids: list[int]):
        
        await self._session.execute(
            delete(self._entity).where(self._entity.id.in_(ids))
        )
        await self._session.commit()
