from collections import defaultdict
from decimal import Decimal

from src.server.handlers.models.production_models import ProductionModel
from src.services import RequiredMaterialsService
from src.storage.repositories import TransactionRepository


class MaterialCheckService:

    def __init__(self):
        self._transaction_repository = TransactionRepository()
        self._required_materials_service = RequiredMaterialsService()

    async def get_missing_materials(
            self,
            production: ProductionModel,
            required_materials: dict[int:Decimal]
    ) -> dict:
        if not required_materials:
            required_materials = await self._required_materials_service.get_required_materials(production)
        available_materials = await self._get_available_materials()
        missing_materials = dict()

        for material_id, required_count in required_materials.items():
            available_count = available_materials.get(material_id, 0)
            if required_count > available_count:
                missing_materials[material_id] = required_count - available_count

        return missing_materials

    async def _get_available_materials(self) -> dict[int, int]:
        dict_available_materials = defaultdict(int)
        available_materials = await self._transaction_repository.get_available_materials()

        for available_material in available_materials:
            dict_available_materials[available_material.material_id] = available_material.count
        return dict_available_materials
