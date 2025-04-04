from src.services.base_service import BaseService

from pydantic import BaseModel

from src.services.exceptions import NotFoundException
from src.services.mappers.entity_mappers  import BaseEntityMapper
from src.storage.repositories import BaseRepository


class BaseEntityService(BaseService):

    def __init__(self):
        self._main_repository = BaseRepository()
        self._main_mapper = BaseEntityMapper()

    async def get_models(self) -> list[BaseModel]:
        return await self.__try_get_models()

    async def __try_get_models(self) -> list[BaseModel]:
        entities = await self._main_repository.get_entities()
        models = self._main_mapper.entities_to_models(entities)
        return models

    async def get_model_by_id(self, entity_id: int) -> BaseModel:
        return await self.__try_get_model_by_id(entity_id)

    async def __try_get_model_by_id(self, entity_id: int) -> BaseModel:
        entity = await self._main_repository.get_entitiy_by_id(entity_id)
        if entity is None:
            raise NotFoundException(entity_id)
        model = self._main_mapper.entity_to_model(entity)
        return model

    async def add_models(self, models: list[BaseModel]) -> list[BaseModel]:
        return await self.__try_add_models(models)

    async def __try_add_models(self, models) -> list[BaseModel]:
        entities = self._main_mapper.models_to_entities(models)
        inserted_entities = await self._main_repository.insert(entities)
        return self._main_mapper.entities_to_models(inserted_entities)

    async def delete_models(self, ids: list[int]):
        await self.__try_delete_models(ids)

    async def __try_delete_models(self, ids: list[int]):
        await self._main_repository.delete(ids)

    async def update_models(self, models: list[BaseModel]) -> list[BaseModel]:
        return await self.__try_update_models(models)

    async def __try_update_models(self, models: list[BaseModel]) -> list[BaseModel]:
        entities = self._main_mapper.models_to_entities(models)
        updated_entities = await self._main_repository.update(entities)
        return self._main_mapper.entities_to_models(updated_entities)
