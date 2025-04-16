from typing import Type

from src.server.handlers.models.product_models import AvailableProductModel
from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import ProductEntityMapper
from src.services.mappers.row_mappers import ProductCostRowMapper
from src.services.utils import EntityServiceFactory, ServiceConfig
from src.storage.repositories import ProductRepository


@EntityServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="product",
        repository=ProductRepository,
        mapper=ProductEntityMapper
    )
)
class ProductService(BaseEntityService):

    def __init__(self, repository: Type[ProductRepository], mapper: Type[ProductEntityMapper]):
        super().__init__(repository, mapper)
        self._product_cost_mapper = ProductCostRowMapper()

    async def get_available_products(self) -> list[AvailableProductModel] | None:
        return await self.__try_get_available_products()

    async def __try_get_available_products(self):
        product_entities = await self._main_repository.get_products_without_order()
        products_id = [product.id for product in product_entities]
        product_cost_entities = await self._main_repository.get_products_costs(products_id)
        return self._product_cost_mapper.entities_to_models(product_cost_entities)
