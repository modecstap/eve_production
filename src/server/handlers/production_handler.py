from src.server.handlers.models import ProductionModel, ProductionCostModel
from src.services import ProductionService


class ProductionHandler:
    def __init__(self):
        self.production_service = ProductionService()

    async def calculate_production_cost(self, product: ProductionModel) -> ProductionCostModel:
        return await self.production_service.calculate_production_cost(product)

    async def create_products(self, products: ProductionModel):
        return await self.production_service.write_production(products)
