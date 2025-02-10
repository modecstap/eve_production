from abc import ABC
from heapq import merge

from sqlalchemy import delete, select
from sqlalchemy.orm import declarative_base

from src.storage.database import Database


class BaseRepository(ABC):
    def __init__(self):
        self.db = Database()
        self._entity: declarative_base = None

    async def get_entities(self) -> list[declarative_base]:
        async with self.db.async_session() as session:
            result = await session.execute(
                select(self._entity)
            )
            return result.scalars().all()

    async def get_entitiy_by_id(self, entity_id: int) -> declarative_base:
        async with self.db.async_session() as session:
            result = await session.execute(
                select(self._entity)
                .where(self._entity.id == entity_id)
            )
            return result.scalars().all()

    async def insert(self, entities) -> list:
        async with self.db.async_session() as session:
            session.add_all(entities)
            await session.flush()
            await session.commit()
            return entities

    async def update(self, transaction_entities):
        async with self.db.async_session() as session:
            await session.execute(
                merge(transaction_entities)
            )
            await session.commit()

    async def delete(self, ids: list[int]):
        async with self.db.async_session() as session:
            await session.execute(
                delete(self._entity).where(self._entity.id.in_(ids))
            )
            await session.commit()
