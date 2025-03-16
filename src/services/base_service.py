from abc import ABC

from pydantic import BaseModel

from src.services.mappers import BaseMapper
from src.storage.repositories import BaseRepository


class BaseService(ABC):

    def __init__(self):
        self._main_repository = BaseRepository()
        self._main_mapper = BaseMapper()

    async def get_models(self) -> list[BaseModel] | None:
        try:
            return await self.__try_get_models()
        except Exception as e:
            await self._main_repository.rollback_transaction()
        finally:
            await self._main_repository.close_transaction()

    async def __try_get_models(self) -> list[BaseModel]:
        await self._main_repository.start_transaction()
        entities = await self._main_repository.get_entities()
        models = self._main_mapper.entities_to_models(entities)
        return models

    async def add_models(self, models: list[BaseModel]):
        try:
            await self.__try_add_models(models)
        except Exception as e:
            await self._main_repository.rollback_transaction()
        finally:
            await self._main_repository.close_transaction()

    async def __try_add_models(self, models):
        await self._main_repository.start_transaction()
        entities = self._main_mapper.models_to_entities(models)
        await self._main_repository.insert(entities)

    async def delete_models(self, ids: list[int]):
        try:
            await self.__try_delete_models(ids)
        except Exception as e:
            await self._main_repository.rollback_transaction()
        finally:
            await self._main_repository.close_transaction()

    async def __try_delete_models(self, ids):
        await self._main_repository.start_transaction()
        await self._main_repository.delete(ids)

    async def update_models(self, models):
        try:
            await self.__try_update_models(models)
        except Exception as e:
            await self._main_repository.rollback_transaction()
        finally:
            await self._main_repository.close_transaction()

    async def __try_update_models(self, models):
        await self._main_repository.start_transaction()
        entities = self._main_mapper.models_to_entities(models)
        await self._main_repository.update(entities)
