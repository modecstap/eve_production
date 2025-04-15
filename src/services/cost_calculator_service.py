from decimal import Decimal

from src.server.handlers.models.production_models import ProductionModel, ProductionCostModel
from src.services import RequiredMaterialsService
from src.services.exceptions import NotEnoughMaterialsException
from src.services.material_check_service import MaterialCheckService
from src.storage.repositories import ProductRepository


class CostCalculatorService:

    def __init__(self):
        self._product_repository = ProductRepository()
        self._material_check_service = MaterialCheckService()
        self.required_materials_service = RequiredMaterialsService()

    async def calculate_production_cost(self, production: ProductionModel) -> ProductionCostModel:
        required_materials = await self.required_materials_service.get_required_materials(production)
        missing_materials = await self._material_check_service.get_missing_materials(production, required_materials)
        if missing_materials:
            raise NotEnoughMaterialsException(missing_materials)

        materials_cost = {}

        for material_id, required_count in required_materials.items():
            materials_cost[material_id] = await self._product_repository.calculate_material_cost(material_id,
                                                                                                 required_count)
        production_cost = sum(materials_cost.values(), Decimal(0))

        return ProductionCostModel(
            materials_cost=materials_cost,
            production_cost=production_cost
        )
