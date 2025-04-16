from src.server.handlers.models import AvailableMaterialModel
from src.services.mappers.row_mappers import AvailableMaterialRowMapper
from src.storage.repositories import TransactionRepository


class AvailableMaterialsService:

    def __init__(self):
        self._transaction_repository = TransactionRepository()
        self._available_material_mapper = AvailableMaterialRowMapper()

    async def get_available_materials(self) -> list[AvailableMaterialModel]:
        entities = await self._transaction_repository.get_available_materials()
        models = self._available_material_mapper.entities_to_models(entities)
        return models
