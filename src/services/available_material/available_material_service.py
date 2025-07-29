from src.services.available_material.available_material_model import AvailableMaterialModel
from src.services.AService import Service
from src.services.mappers.row_mappers import AvailableMaterialRowMapper
from src.services.utils import ServiceConfig, ServiceFactory
from src.storage.repositories import BaseRepository
from src.storage.repositories.available_material_repository import AvailableMaterialsRepository
from src.storage.tables import Transaction


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="available_material",
    )
)
class AvailableMaterialsService(Service):

    def __init__(
            self,
            materials_repository: AvailableMaterialsRepository = AvailableMaterialsRepository(),
            available_material_mapper: AvailableMaterialRowMapper = AvailableMaterialRowMapper()
    ):
        self._materials_repository = materials_repository
        self._available_material_mapper = available_material_mapper

    async def do(self, model = None) -> list[AvailableMaterialModel]:
        material_entities = await self._materials_repository.get_entities()
        material_models = self._available_material_mapper.entities_to_models(material_entities)
        return material_models
