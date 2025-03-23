from collections import defaultdict
from decimal import Decimal, ROUND_UP

from src.server.handlers.models import ProductModel, AvailableProductModel, ProductionCostModel
from src.services.enetity_serice import BaseEntityService
from src.services.exceptions import NotEnoughMaterialsException
from src.services.mappers.entity_mappers  import ProductEntityMapper
from src.services.mappers.row_mappers import ProductCostRowMapper
from src.storage.repositories import ProductRepository, MaterialListRepository, TransactionRepository, StationRepository


class ProductService(BaseEntityService):

    def __init__(self):
        super().__init__()
        self._main_repository = ProductRepository()
        self._material_list_repository = MaterialListRepository()
        self._transaction_repository = TransactionRepository()
        self._station_repository = StationRepository()

        self._main_mapper = ProductEntityMapper()
        self._product_cost_mapper = ProductCostRowMapper()

    async def get_available_products(self) -> list[AvailableProductModel] | None:
        return await self.__try_get_available_products()

    async def __try_get_available_products(self):
        product_entities = await self._main_repository.get_products_without_order()
        products_id = [product.id for product in product_entities]
        product_cost_entities = await self._main_repository.get_products_costs(products_id)
        return self._product_cost_mapper.entities_to_models(product_cost_entities)
