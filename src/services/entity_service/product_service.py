from src.server.handlers.models.product_models import AvailableProductModel, ProductModel
from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.services.mappers.row_mappers import ProductCostRowMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import Product


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="product",
    )
)
class ProductService(BaseEntityService):

    def __init__(
            self,
            repository: BaseRepository = BaseRepository(Product),
            mapper: BaseEntityMapper = BaseEntityMapper(ProductModel, Product),
            product_cost_mapper: ProductCostRowMapper = ProductCostRowMapper()
    ):
        super().__init__(repository, mapper)
        self._product_cost_mapper = product_cost_mapper

    async def get_available_products(self) -> list[AvailableProductModel] | None:
        return await self.__try_get_available_products()

    async def __try_get_available_products(self):
        product_entities = await self._main_repository.get_products_without_order()
        products_id = [product.id for product in product_entities]
        product_cost_entities = await self._main_repository.get_products_costs(products_id)
        return self._product_cost_mapper.entities_to_models(product_cost_entities)
