from src.server.handlers.models.production_models import ProductionModel
from src.services.cost_calculator_service import CostCalculatorService
from src.services.base_service import BaseService
from src.services.mappers import ProductionMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import TransactionRepository, ProductRepository
from src.storage.tables import Transaction

@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="production",
    )
)
class ProductionService(BaseService):

    def __init__(self):
        self._main_mapper: ProductionMapper = ProductionMapper()
        self._transaction_repository = TransactionRepository()
        self._product_repository = ProductRepository()
        self._cost_calculator_service = CostCalculatorService()

    async def write_production(self, production: ProductionModel):
        async with self._product_repository.create_session() as session:
            production_cost = await self._cost_calculator_service.calculate_production_cost(production)
            product_entity = self._main_mapper.model_to_entity(production)
            await self._product_repository.insert([product_entity], session=session)
            await self._product_repository.insert_used_transactions(product_entity, production.count, session=session)
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
