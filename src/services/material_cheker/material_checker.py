from itertools import count

from pydantic import BaseModel

from src.server.handlers.models.production_models import ProductionModel
from src.services import RequiredMaterialsService
from src.services.AService import Service
from src.services.available_material.available_material_service import AvailableMaterialsService
from src.services.exceptions import NotEnoughMaterialsException
from src.services.material_cheker.material_checker_payload import MaterialCheckerPayload
from src.services.required_material.required_materials_payload import RequiredMaterialsPayload
from src.services.utils import ServiceFactory, ServiceConfig


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="material_check",
    )
)
class MaterialChecker(Service):

    def __init__(self):
        self._available_materials_service = AvailableMaterialsService()
        self._required_materials_service = RequiredMaterialsService()

    async def do(self, model: MaterialCheckerPayload) -> None:
        required_materials = await self._required_materials_service.do(
            RequiredMaterialsPayload(
            product_type_id=model.type_id,
            count=model.count,
            blueprint_efficiency=model.blueprint_efficiency
        ))
        available_materials = await self._available_materials_service.do()
        missing_materials = dict()

        for required_material_id, required_count in required_materials.items():
            available_count = [
                available_material.count for available_material in available_materials
                if available_material.material_id == required_material_id
            ]
            if required_count > available_count:
                missing_materials[required_material_id] = required_count - available_count
        if missing_materials:
            raise NotEnoughMaterialsException(missing_materials)

