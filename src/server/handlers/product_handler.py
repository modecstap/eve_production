from aiohttp.web import Request

from src.server.handlers.models import ProductModel
from src.services import ProductService


class ProductHandler:
    def __init__(self):
        self.product_service = ProductService()

    async def get_products(self, request: Request):
        return await self.product_service.get_models()

    async def get_available_products(self, request: Request):
        return await self.product_service.get_available_products()

    async def create_products(self, request: Request, products: list[ProductModel]):
        await self.product_service.create_products(products)
