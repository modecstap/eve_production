from src.server.handlers.models import AvailableMaterialModel
from src.services import BaseService
from src.services.mappers import TransactionMapper, AvailableMaterialRowMapper
from src.storage.repositories import TransactionRepository


class TransactionService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = TransactionRepository()
        self._main_mapper = TransactionMapper()
        self._available_material_mapper = AvailableMaterialRowMapper()

    async def get_available_materials(self) -> list[AvailableMaterialModel]:
        return await self.__try_get_available_materials()

    async def __try_get_available_materials(self):
        entities = await self._main_repository.get_available_materials()
        models = self._available_material_mapper.entities_to_models(entities)
        return models
