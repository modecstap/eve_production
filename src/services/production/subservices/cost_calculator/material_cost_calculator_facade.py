from src.services.AService import Service
from src.services.production.subservices.chekers.material_checker.material_checker_mediator import MaterialCheckerMediator
from src.services.production.subservices.cost_calculator.cost_calculator import CostCalculator
from src.services.production.models.production_cost import ProductionCostModel
from src.services.production.models.production_info import ProductionInfo
from src.services.production.subservices.required_material.required_materials_service import RequiredMaterialsService
from src.services.utils import ServiceFactory, ServiceConfig


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="cost_calculator",
    )
)
class MaterialCostCalculatorFacade(Service):
    """
    объединяет логику получения материалов, проверки и расчета стоимости.
    """

    def __init__(
            self,
            required_materials_service: RequiredMaterialsService = RequiredMaterialsService(),
            cost_calculator: CostCalculator = CostCalculator()
    ):
        self._required_materials_service = required_materials_service
        self._cost_calculator = cost_calculator

    async def do(self, production: ProductionInfo) -> ProductionCostModel:
        required_materials = await self._required_materials_service.do(production)

        await MaterialCheckerMediator().check(required_materials)
        cost = await self._cost_calculator.do(required_materials)

        return cost
