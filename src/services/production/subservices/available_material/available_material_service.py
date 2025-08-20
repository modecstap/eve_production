from src.services.AService import Service
from src.services.production.models.available_material import AvailableMaterial
from src.services.production.models.available_materials import AvailableMaterials
from src.services.utils import ServiceConfig, ServiceFactory
from src.storage.repositories.available_material_repository import AvailableMaterialsRepository


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="available_material",
    )
)
class AvailableMaterialsService(Service):

    def __init__(
            self,
            materials_repository: AvailableMaterialsRepository = AvailableMaterialsRepository(),
    ):
        self._materials_repository = materials_repository

    async def do(self, model = None) -> AvailableMaterials:
        material_entities = await self._materials_repository.get_entities()

        materials: dict[int, AvailableMaterial] = dict()
        for material in material_entities:
            materials[material.material_id] = AvailableMaterial(
                material_id=material.material_id,
                name=material.name,
                count=material.count,
                mean_price=material.mean_price
            )
        return AvailableMaterials(materials=materials)
