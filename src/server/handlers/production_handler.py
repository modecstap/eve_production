from src.server.handlers.models.production_models import ProductionModel
from src.services import ProductionService


class ProductionHandler:
    def __init__(self):
        self.production_service = ProductionService()

    async def create_products(self, products: ProductionModel):
        return await self.production_service.write_production(products)
