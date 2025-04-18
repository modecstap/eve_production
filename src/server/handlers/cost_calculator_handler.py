from src.server.handlers.models.production_models import ProductionModel, ProductionCostModel
from src.services.utils import ServiceFactory


class CostCalculatorHandler:
    def __init__(self):
        self.cost_calculator_service = ServiceFactory.get_entity_service("cost_calculator")

    async def calculate_production_cost(self, product: ProductionModel) -> ProductionCostModel:
        return await self.cost_calculator_service.calculate_production_cost(product)
