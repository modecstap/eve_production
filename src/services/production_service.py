from collections import defaultdict
from decimal import Decimal, ROUND_UP

from src.server.handlers.models import ProductionModel, ProductionCostModel
from src.services.base_service import BaseService
from src.services.exceptions import NotEnoughMaterialsException
from src.services.mappers import ProductionMapper
from src.storage.repositories import StationRepository, MaterialListRepository, TransactionRepository, ProductRepository
from src.storage.tables import Station, MaterialList, Transaction


class ProductionService(BaseService):

    def __init__(self):
        self._main_mapper: ProductionMapper = ProductionMapper()
        self._station_repository = StationRepository()
        self._material_list_repository = MaterialListRepository()
        self._transaction_repository = TransactionRepository()
        self._product_repository = ProductRepository()

    async def write_production(self, production: ProductionModel):
        if not await self._materials_is_available(production):
            raise NotEnoughMaterialsException()

        session = self._product_repository.create_session()
        try:
            await self.__try_write_product(production, session)
        except Exception as e:
            await session.rollback()
        finally:
            await session.close()

    async def __try_write_product(self, production, session):
        product_entity = self._main_mapper.model_to_entity(production)
        await self._product_repository.insert([product_entity], session=session)
        await self._product_repository.insert_with_used_transaction(product_entity, production.count, session=session)
        production_cost = await self.calculate_production_cost(production)
        product_transaction = Transaction(
            release_date=production.release_date,
            material_id=production.type_id,
            product_id=product_entity.id,
            count=production.count,
            price=production_cost.production_cost,
            remains=production.count
        )
        await self._transaction_repository.insert([product_transaction], session=session)
        await session.commit()

    async def _materials_is_available(self, production: ProductionModel):
        required_materials = await self._get_required_materials(production)
        available_materials = await self._get_available_materials()

        for material_id, required_count in required_materials.items():
            if required_count > available_materials.get(material_id, 0):
                return False

        return True

    async def _get_required_materials(self, production: ProductionModel) -> dict:
        required_materials = defaultdict(int)
        materials_list = await self._material_list_repository.get_materials_by_type_id(production.type_id)
        station = await self._station_repository.get_entitiy_by_id(production.station_id)

        for material in materials_list:
            required_materials[material.material_id] += \
                await self._get_corrected_mateial_count(
                    material,
                    production,
                    station
                )
        return required_materials

    async def _get_corrected_mateial_count(
            self,
            material: MaterialList,
            production: ProductionModel,
            station: Station
    ) -> Decimal:
        return (
                material.need_count
                * production.blueprint_efficiency
                * station.material_efficiency
                * production.count
        ).quantize(Decimal('1.'), rounding=ROUND_UP)

    async def _get_available_materials(self) -> dict:
        dict_available_materials = defaultdict(int)
        available_materials = await self._transaction_repository.get_available_materials()

        for available_material in available_materials:
            dict_available_materials[available_material.material_id] = available_material.count
        return dict_available_materials

    async def calculate_production_cost(self, production: ProductionModel) -> ProductionCostModel:
        try:
            return await self.__try_calculate_production_cost(production)
        except NotEnoughMaterialsException as e:
            raise e

    async def __try_calculate_production_cost(self, production: ProductionModel):
        if await self._materials_is_available(production):
            materials_cost = {}

            required_materials = await self._get_required_materials(production)
            for material_id, required_count in required_materials.items():
                materials_cost[material_id] = await self._product_repository.calculate_material_cost(material_id,required_count)

            production_cost = Decimal(0)
            for cost in materials_cost.values():
                production_cost += cost

            return ProductionCostModel(
                materials_cost=materials_cost,
                production_cost=production_cost
            )
        else:
            raise NotEnoughMaterialsException()
