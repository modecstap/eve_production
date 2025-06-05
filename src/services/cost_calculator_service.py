from decimal import Decimal

from src.server.handlers.models.production_models import ProductionModel, ProductionCostModel
from src.services import RequiredMaterialsService
from src.services.exceptions import NotEnoughMaterialsException
from src.services.material_check_service import MaterialCheckService
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import Product


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="cost_calculator",
    )
)
class CostCalculatorService:

    def __init__(
            self,
            product_repository: BaseRepository = BaseRepository(Product),
            material_check_service: MaterialCheckService = MaterialCheckService(),
            required_materials_service: RequiredMaterialsService = RequiredMaterialsService()
    ):
        self._product_repository = product_repository
        self._material_check_service = material_check_service
        self._required_materials_service = required_materials_service

    async def calculate_production_cost(self, production: ProductionModel) -> ProductionCostModel:
        required_materials = await self._required_materials_service.get_required_materials(production)
        missing_materials = await self._material_check_service.get_missing_materials(production)
        if missing_materials:
            raise NotEnoughMaterialsException(missing_materials)

        materials_cost = {}

        for material_id, required_count in required_materials.items():
            materials_cost[material_id] = await self._product_repository.execute_query(
                query="SELECT calculate_material_cost(:p_material_id, :p_need_count)",
                params={"p_material_id": material_id, "p_need_count": required_count}
            )
        production_cost = sum(materials_cost.values(), Decimal(0))

        return ProductionCostModel(
            materials_cost=materials_cost,
            production_cost=production_cost
        )
