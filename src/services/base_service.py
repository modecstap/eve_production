from abc import ABC

from pydantic import BaseModel

from src.mappers import BaseMapper
from src.storage.repositories import BaseRepository


class BaseService(ABC):

    def __init__(self):
        self._main_repository = BaseRepository()
        self._main_mapper = BaseMapper()

    async def get_models(self) -> list[BaseModel]:
        entities = await self._main_repository.get_entities()
        models = self._main_mapper.entities_to_models(entities)
        return models

    async def add_models(self, models: list[BaseModel]):
        entities = self._main_mapper.models_to_entities(models)
        await self._main_repository.insert(entities)

    async def delete_models(self, ids: list[int]):
        await self._main_repository.delete(ids)

    async def update_models(self, models):
        entities = self._main_mapper.models_to_entities(models)
        await self._main_repository.update(entities)
