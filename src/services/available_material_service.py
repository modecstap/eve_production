from typing import Type

from src.server.handlers.models import AvailableMaterialModel
from src.services.base_service import BaseService
from src.services.mappers.row_mappers import AvailableMaterialRowMapper
from src.services.utils import ServiceConfig, ServiceFactory
from src.storage.repositories import TransactionRepository

@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="available_materials",
    )
)
class AvailableMaterialsService(BaseService):

    def __init__(
            self,
            transaction_repository: TransactionRepository=TransactionRepository(),
            available_material_mapper: AvailableMaterialRowMapper=AvailableMaterialRowMapper()
    ):
        self._transaction_repository = transaction_repository
        self._available_material_mapper = available_material_mapper

    async def get_available_materials(self) -> list[AvailableMaterialModel]:
        entities = await self._transaction_repository.get_available_materials()
        models = self._available_material_mapper.entities_to_models(entities)
        return models
