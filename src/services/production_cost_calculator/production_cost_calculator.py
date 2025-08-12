from decimal import Decimal

from src.services.cost_calculator.material_cost_calculator_facade import MaterialCostCalculatorFacade
from src.services.mappers.production_cost_to_material_cost_mapper import ProductionCostToMaterialCostMapper
from src.services.production_cost_calculator.production_cost_payload import ProductionCostPayload


class ProductionCostCalculator:
    """
    Считает полную себестоимость произведённых товаров.
    """

    def __init__(self):
        self._material_cost_calculator = MaterialCostCalculatorFacade()
        self._material_cost_mapper = ProductionCostToMaterialCostMapper()

    async def calculate(self, payload: ProductionCostPayload) -> Decimal:
        material_cost_payload = await self._material_cost_mapper.map(payload)
        material_cost = await self._material_cost_calculator.do(material_cost_payload)

        result_cost = material_cost + payload.production_cost

        return result_cost
