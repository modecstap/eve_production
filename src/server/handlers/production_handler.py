from src.server.handlers.models.production_models import ProductionMediatorModel
from src.services.utils import ServiceFactory


class ProductionHandler:
    def __init__(self):
        self.production_service = ServiceFactory.get_service("production")

    async def create_products(self, products: ProductionMediatorModel):
        return await self.production_service.do(products)
