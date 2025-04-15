from src.server.handlers.models.production_models import ProductionModel
from src.services import CostCalculatorService
from src.services.base_service import BaseService
from src.services.exceptions import NotEnoughMaterialsException
from src.services.mappers import ProductionMapper
from src.services.material_check_service import MaterialCheckService
from src.storage.repositories import TransactionRepository, ProductRepository
from src.storage.tables import Transaction


class ProductionService(BaseService):

    def __init__(self):
        self._main_mapper: ProductionMapper = ProductionMapper()
        self._transaction_repository = TransactionRepository()
        self._product_repository = ProductRepository()
        self._material_checker = MaterialCheckService()
        self._cost_calculator_service = CostCalculatorService()

    async def write_production(self, production: ProductionModel):
        missing_materials: dict = await self._material_checker.get_missing_materials(production)
        if missing_materials:
            raise NotEnoughMaterialsException(missing_materials)

        async with self._product_repository.create_session() as session:
            await self._try_write_product(production, session)

    async def _try_write_product(self, production, session):
        product_entity = self._main_mapper.model_to_entity(production)
        await self._product_repository.insert([product_entity], session=session)
        await self._product_repository.insert_used_transactions(product_entity, production.count, session=session)
        production_cost = await self._cost_calculator_service.calculate_production_cost(production)
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
