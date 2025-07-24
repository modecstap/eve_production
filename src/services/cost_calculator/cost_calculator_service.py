from decimal import Decimal


from src.server.handlers.models.production_models import ProductionModel
from src.services import RequiredMaterialsService
from src.services.AService import Service
from src.services.cost_calculator.cost_model import CostModel
from src.services.material_cheker.material_checker import MaterialChecker
from src.services.material_cheker.material_checker_payload import MaterialCheckerPayload
from src.services.required_material.required_materials_payload import RequiredMaterialsPayload
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import Product


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="cost_calculator",
    )
)
class CostCalculatorService(Service):

    def __init__(
            self,
            product_repository: BaseRepository = BaseRepository(Product),
            material_checker: MaterialChecker = MaterialChecker(),
            required_materials_service: RequiredMaterialsService = RequiredMaterialsService()
    ):
        self._product_repository = product_repository
        self._material_checker = material_checker
        self._required_materials_service = required_materials_service

    async def do(self, production: ProductionModel) -> CostModel:
        await self._material_checker.do(MaterialCheckerPayload(
            product_type_id=production.type_id,
            count=production.count,
            blueprint_efficiency=production.blueprint_efficiency,
        ))
        required_materials = await self._required_materials_service.do(RequiredMaterialsPayload(
            product_type_id=production.type_id,
            count=production.count,
            blueprint_efficiency=production.blueprint_efficiency
        ))

        materials_cost = {}

        for material_id, required_count in required_materials.items():
            materials_cost[material_id] = await self._product_repository.execute_query(
                query="SELECT calculate_material_cost(:p_material_id, :p_need_count)",
                params={"p_material_id": material_id, "p_need_count": required_count}
            )
        production_cost = sum(materials_cost.values(), Decimal(0))

        return CostModel(
            materials_cost=materials_cost,
            production_cost=production_cost
        )
