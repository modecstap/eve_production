from decimal import Decimal
from typing import Type

from src.services.AService import Service
from src.server.handlers.models.production_models import ProductionModel
from src.services.required_material.required_materials_service import RequiredMaterialsService
from src.services.chekers.material_checker.material_checker_mediator import MaterialCheckerMediator
from src.services.cost_calculator.cost_model import CostModel
from src.services.mappers.production_to_required_materials import ProductionToRequiredMaterialsMapper
from src.services.mappers.required_materials_to_material_cheker import RequiredMaterialsToMaterialsCheckerMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import Product


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="cost_calculator",
    )
)
class CostCalculatorService(Service):
    # TODO из этого класса сделать посредник и вынести логику подсчёта в другой класс
    """
    Считает цену производства продукта.
    """


    def __init__(
            self,
            product_repository: BaseRepository = BaseRepository(Product),
            required_materials_service: RequiredMaterialsService = RequiredMaterialsService(),
            material_checker: Type[MaterialCheckerMediator] = MaterialCheckerMediator,
    ):
        self._product_repository = product_repository
        self._material_checker = material_checker
        self._required_materials_service = required_materials_service

    async def do(self, production: ProductionModel) -> CostModel:
        required_material_payload = ProductionToRequiredMaterialsMapper(production).map()
        required_materials = await self._required_materials_service.do(required_material_payload)
        check_payload = RequiredMaterialsToMaterialsCheckerMapper(required_materials).map()
        await self._material_checker(check_payload).check()

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
