from decimal import Decimal, ROUND_UP

from src.server.handlers.models import ProductModel, AvailableProductModel, ProductionCostModel
from src.services import BaseService
from src.services.mappers import ProductMapper, ProductCostRowMapper
from src.services.exceptions import NotEnoughMaterialsException
from src.storage.repositories import ProductRepository, MaterialListRepository, TransactionRepository, StationRepository

from collections import defaultdict


class ProductService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = ProductRepository()
        self._material_list_repository = MaterialListRepository()
        self._transaction_repository = TransactionRepository()
        self._station_repository = StationRepository()

        self._main_mapper = ProductMapper()
        self._product_cost_mapper = ProductCostRowMapper()

    async def get_available_products(self) -> list[AvailableProductModel]:
        product_entities = await self._main_repository.get_products_without_order()
        products_id = [product.id for product in product_entities]
        product_cost_entities = await self._main_repository.get_products_costs(products_id)
        return self._product_cost_mapper.entities_to_models(product_cost_entities)

    async def create_products(self, products: list[ProductModel]):
        if await self._materials_is_available(products):
            product_entities = self._main_mapper.models_to_entities(products)
            await self._main_repository.insert_with_used_transaction(product_entities)
        else:
            raise NotEnoughMaterialsException()

    async def _materials_is_available(self, products: list[ProductModel]):
        required_materials = await self._get_products_required_materials(products)
        available_materials = await self._get_available_materials()

        for material_id, required_count in required_materials.items():
            if (material_id not in available_materials.keys()
                    or required_count > available_materials[material_id]):
                return False

        return True

    async def _get_products_required_materials(self, products) -> dict:
        list_required_materials = [await self._get_product_required_materials(product) for product in products]
        required_materials = self._merge_required_materials(list_required_materials)
        return required_materials

    async def _get_product_required_materials(self, product: ProductModel) -> dict:
        required_materials = defaultdict(int)
        materials_list = await self._material_list_repository.get_materials_by_type_id(product.type_id)
        station_material_efficiency = await self._station_repository.get_station_material_efficiency(
            product.station_id)

        for material in materials_list:
            required_materials[material.material_id] += await self._get_corrected_mateial_count(material, product,
                                                                                                station_material_efficiency)
        return required_materials

    async def _get_corrected_mateial_count(self, material, product, station_material_efficiency):
        return (
                material.need_count * product.blueprint_efficiency * station_material_efficiency
        ).quantize(Decimal('1.'), rounding=ROUND_UP)

    async def _get_available_materials(self):
        dict_available_materials = defaultdict(int)
        available_materials = await self._transaction_repository.get_available_materials()
        for available_material in available_materials:
            dict_available_materials[available_material.material_id] = available_material.count
        return dict_available_materials

    def _merge_required_materials(self, list_required_materials: list[dict]):
        merged_required_materials = defaultdict(int)
        for required_materials in list_required_materials:
            for material_id, required_count in required_materials.items():
                merged_required_materials[material_id] += required_count
        return merged_required_materials

    async def calculate_production_cost(self, product: ProductModel) -> ProductionCostModel:
        if await self._materials_is_available([product]):
            materials_cost = {}

            required_materials = await self._get_product_required_materials(product)
            for material_id, required_count in required_materials.items():
                materials_cost[material_id] = await self._main_repository.calculate_material_cost(material_id, required_count)

            production_cost = sum(materials_cost.values())

            return ProductionCostModel(
                materials_cost=materials_cost,
                production_cost=production_cost
            )
        else:
            raise NotEnoughMaterialsException()
