from src.server.handlers.models import ProductModel, ProductionCostModel
from src.services.enetity_serice import ProductService


class ProductHandler:
    def __init__(self):
        self.product_service = ProductService()

    async def get_products(self):
        return await self.product_service.get_models()

    async def get_available_products(self):
        return await self.product_service.get_available_products()

    async def calculate_production_cost(self, product: ProductModel) -> ProductionCostModel:
        return await self.product_service.calculate_production_cost(product)

    async def create_products(self, products: list[ProductModel]):
        return await self.product_service.create_products(products)
