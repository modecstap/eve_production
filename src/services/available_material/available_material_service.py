from src.services.available_material.available_material_model import AvailableMaterialModel
from src.services.AService import Service
from src.services.mappers.row_mappers import AvailableMaterialRowMapper
from src.services.utils import ServiceConfig, ServiceFactory
from src.storage.repositories import TransactionRepository


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="available_material",
    )
)
class AvailableMaterialsService(Service):

    def __init__(
            self,
            transaction_repository: TransactionRepository = TransactionRepository(),
            available_material_mapper: AvailableMaterialRowMapper = AvailableMaterialRowMapper()
    ):
        self._transaction_repository = transaction_repository
        self._available_material_mapper = available_material_mapper

    async def do(self, model = None) -> list[AvailableMaterialModel]:
        entities = await self._transaction_repository.get_available_materials()
        models = self._available_material_mapper.entities_to_models(entities)
        return models
