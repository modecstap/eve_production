from src.server.handlers.models import ProductModel, ProductionCostModel
from src.services.enetity_serice import ProductService


class ProductHandler:
    def __init__(self):
        self.product_service = ProductService()

    async def get_products(self):
        return await self.product_service.get_models()

    async def get_available_products(self):
        return await self.product_service.get_available_products()
