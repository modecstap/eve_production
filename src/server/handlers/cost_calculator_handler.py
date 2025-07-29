from src.server.handlers.models.production_models import ProductionMediatorModel
from src.services.cost_calculator.cost_model import CostModel
from src.services.utils import ServiceFactory


class CostCalculatorHandler:
    def __init__(self):
        self.cost_calculator_service = ServiceFactory.get_service("cost_calculator")

    async def calculate_production_cost(self, product: ProductionMediatorModel) -> CostModel:
        return await self.cost_calculator_service.do(product)
