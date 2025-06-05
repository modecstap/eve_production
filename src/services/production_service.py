from src.server.handlers.models.production_models import ProductionModel
from src.services.base_service import BaseService
from src.services.cost_calculator_service import CostCalculatorService
from src.services.mappers import ProductionMapper
from src.services.production_builder import ProductionBuilder
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import TransactionRepository, BaseRepository
from src.storage.tables import Product


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="production",
    )
)
class ProductionService(BaseService):
    def __init__(
            self,
            mapper: ProductionMapper = ProductionMapper(),
            product_repo: BaseRepository = BaseRepository(Product),
            transaction_repo: TransactionRepository = TransactionRepository(),
            cost_calculator: CostCalculatorService = CostCalculatorService(),
            builder: ProductionBuilder = ProductionBuilder(),
    ):
        self._mapper = mapper
        self._product_repo = product_repo
        self._transaction_repo = transaction_repo
        self._cost_calculator = cost_calculator
        self._builder = builder

    async def write_production(self, production: ProductionModel):
        async with self._product_repo.create_session() as session:
            product, transaction = await self._builder.build(production)

            await self._product_repo.insert([product], session=session)
            await self._product_repo.execute_query(
                query="SELECT create_used_transaction(:input_product_id, :input_count)",
                params={"input_product_id": product.id, "input_count": production.count},
                session=session
            )
            await self._transaction_repo.insert([transaction], session=session)

            await session.commit()
