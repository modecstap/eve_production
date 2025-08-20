from src.services.production.models.Responces.check_response import CheckResponse
from src.services.production.models.production_info import ProductionInfo
from src.services.production.models.reqired_materials import RequiredMaterials
from src.services.production.subservices.chekers.material_checker.material_checker_mediator import MaterialCheckerMediator
from src.services.production.models.production_cost import ProductionCostModel
from src.services.production.subservices.production_cost_calculator.production_cost_calculator import \
    ProductionCostCalculator
from src.services.production.subservices.required_material.required_materials_service import RequiredMaterialsService
from src.services.production_writer.production_service import ProductionService


class Production:

    def __init__(self, payload: ProductionInfo):
        self._payload = payload

    async def calculate_required_materials(self) -> RequiredMaterials:
        return await RequiredMaterialsService().do(self._payload)

    async def chek_materials_availability(self) -> CheckResponse:
        required_materials = await RequiredMaterialsService().do(self._payload)
        await MaterialCheckerMediator().check(required_materials)
        return CheckResponse(possible_to_produce=True)

    async def calculate_production_cost(self) -> ProductionCostModel:
        return await ProductionCostCalculator().calculate(self._payload)

    async def make_product(self):
        required_materials = await RequiredMaterialsService().do(self._payload)

        await MaterialCheckerMediator().check(required_materials)

        await ProductionService().do(self._payload)

