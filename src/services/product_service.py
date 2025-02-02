from src.mappers import ProductMapper
from src.server.handlers.models import ProductModel, AvailableProductModel
from src.services import BaseService
from src.storage.repositories import ProductRepository


class ProductService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = ProductRepository()
        self._main_mapper = ProductMapper()

    async def get_available_products(self) -> list[AvailableProductModel]:
        product_entities = await self._main_repository.get_products_without_order()
        products_id = [product.id for product in product_entities]
        products_costs = await self._main_repository.get_products_costs(products_id)
        return self._main_mapper.products_costs_to_models(products_costs)

    async def create_products(self, products: list[ProductModel]):
        product_entities = self._main_mapper.models_to_entities(products)
        await self._main_repository.insert_with_used_transaction(product_entities)
