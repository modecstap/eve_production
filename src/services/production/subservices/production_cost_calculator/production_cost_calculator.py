from src.services.production.models.production_cost import ProductionCostModel
from src.services.production.models.production_info import ProductionInfo
from src.services.production.subservices.cost_calculator.material_cost_calculator_facade import MaterialCostCalculatorFacade


class ProductionCostCalculator:
    """
    Считает полную себестоимость произведённых товаров.
    """

    def __init__(self):
        self._material_cost_calculator = MaterialCostCalculatorFacade()

    async def calculate(self, payload: ProductionInfo) -> ProductionCostModel:
        material_cost = await self._material_cost_calculator.do(payload)
        material_cost.production_cost = material_cost + payload.production_cost
        return material_cost
