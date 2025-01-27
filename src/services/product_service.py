from src.mappers import ProductMapper
from src.server.handlers.models import ProductModel
from src.services import BaseService
from src.storage.repositories import ProductRepository


class ProductService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = ProductRepository()
        self._main_mapper = ProductMapper()

    async def create_products(self, products: list[ProductModel]):
        product_entities = self._main_mapper.models_to_entities(products)
        await self._main_repository.insert_with_used_transaction(product_entities)
