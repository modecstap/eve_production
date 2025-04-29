from collections import defaultdict

from src.server.handlers.models.production_models import ProductionModel
from src.services import RequiredMaterialsService, AvailableMaterialsService
from src.services.utils import ServiceFactory, ServiceConfig

@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="material_check",
    )
)
class MaterialCheckService:

    def __init__(self):
        self._available_materials_service = AvailableMaterialsService()
        self._required_materials_service = RequiredMaterialsService()

    async def get_missing_materials(
            self,
            production: ProductionModel,
    ) -> dict:
        required_materials = await self._required_materials_service.get_required_materials(production)
        available_materials = await self._available_materials_service.get_available_materials()
        missing_materials = dict()

        for material_id, required_count in required_materials.items():
            available_count = [
                available_material.count for available_material in  available_materials
                if available_material.material_id == material_id
            ]
            if required_count > available_count:
                missing_materials[material_id] = required_count - available_count

        return missing_materials
