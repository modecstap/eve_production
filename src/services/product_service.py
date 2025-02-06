from src.server.handlers.models import ProductModel, AvailableProductModel
from src.services import BaseService
from src.services.mappers import ProductMapper, ProductCostRowMapper
from src.storage.repositories import ProductRepository


class ProductService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = ProductRepository()
        self._main_mapper = ProductMapper()
        self._product_cost_mapper = ProductCostRowMapper()

    async def get_available_products(self) -> list[AvailableProductModel]:
        product_entities = await self._main_repository.get_products_without_order()
        products_id = [product.id for product in product_entities]
        product_cost_entities = await self._main_repository.get_products_costs(products_id)
        return self._product_cost_mapper.entities_to_models(product_cost_entities)

    async def create_products(self, products: list[ProductModel]):
        product_entities = self._main_mapper.models_to_entities(products)
        await self._main_repository.insert_with_used_transaction(product_entities)
