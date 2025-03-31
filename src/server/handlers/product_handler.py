from src.server.handlers.models.product_models import ProductModel, AvailableProductModel
from src.services.entity_service import ProductService


class ProductHandler:
    def __init__(self):
        self.product_service = ProductService()

    async def get_products(self) -> list[ProductModel]:
        return await self.product_service.get_models()

    async def get_available_products(self) -> list[AvailableProductModel]:
        return await self.product_service.get_available_products()
