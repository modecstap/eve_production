from src.services.AService import Service
from src.services.chekers.material_checker.material_checker_mediator import MaterialCheckerMediator
from src.services.cost_calculator.cost_calculator import CostCalculator
from src.services.cost_calculator.cost_model import CostModel
from src.services.cost_calculator.production_facade_model import CostCalculatorFacadeModel
from src.services.mappers.production_to_required_materials import ProductionToRequiredMaterialsMapper
from src.services.mappers.required_materials_to_material_cheker import RequiredMaterialsToMaterialsCheckerMapper
from src.services.required_material.required_materials_service import RequiredMaterialsService
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

    async def do(self, production: CostCalculatorFacadeModel) -> CostModel:
        required_material_payload = ProductionToRequiredMaterialsMapper().map(production)
        required_materials = await self._required_materials_service.do(required_material_payload)

        check_payload = RequiredMaterialsToMaterialsCheckerMapper().map(required_materials)
        await MaterialCheckerMediator(check_payload).check()

        cost = await self._cost_calculator.do(required_materials)

        return cost
