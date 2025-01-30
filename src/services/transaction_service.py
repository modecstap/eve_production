from src.mappers import TransactionMapper
from src.services import BaseService
from src.storage.repositories import TransactionRepository


class TransactionService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = TransactionRepository()
        self._main_mapper = TransactionMapper()

    async def get_available_materials(self):
        entities = await self._main_repository.get_available_materials()
        models = self._main_mapper.available_material_entities_to_models(entities)
        return models
