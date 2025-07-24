from pydantic import BaseModel

from src.services.exceptions import NotFoundException
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.storage.repositories import BaseRepository


class BaseEntityService:

    def __init__(
            self,
            repository: BaseRepository,
            mapper: BaseEntityMapper
    ):
        self._main_repository: BaseRepository = repository
        self._main_mapper: BaseEntityMapper = mapper

    async def get_models(self) -> list[BaseModel]:
        entities = await self._main_repository.get_entities()
        models = self._main_mapper.entities_to_models(entities)
        return models

    async def get_model_by_id(self, entity_id: int) -> BaseModel:
        entity = await self._main_repository.get_entity_by_id(entity_id)
        if entity is None:
            raise NotFoundException(entity_id)
        model = self._main_mapper.entity_to_model(entity)
        return model

    async def add_models(self, models: list[BaseModel]) -> list[BaseModel]:
        entities = self._main_mapper.models_to_entities(models)
        inserted_entities = await self._main_repository.insert(entities)
        return self._main_mapper.entities_to_models(inserted_entities)

    async def delete_models(self, ids: list[int]):
        await self._main_repository.delete(ids)

    async def update_models(self, models: list[BaseModel]) -> list[BaseModel]:
        entities = self._main_mapper.models_to_entities(models)
        updated_entities = await self._main_repository.update(entities)
        return self._main_mapper.entities_to_models(updated_entities)
