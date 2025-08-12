from src.services.AService import Service

from src.services.production.production_payload import ProductionPayload
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.repositories.product_usage_repository import ProductUsageRepository
from src.storage.tables import Product, Transaction


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="production",
    )
)
class ProductionService(Service):
    """
    Записывает данные о произведённых продуктах
    """

    def __init__(
            self,
            product_repo: BaseRepository = BaseRepository(Product),
            transaction_repo: BaseRepository = BaseRepository(Transaction),
            product_usage_repo: ProductUsageRepository = ProductUsageRepository()
    ):
        self._product_repo = product_repo
        self._transaction_repo = transaction_repo
        self._product_usage_repo = product_usage_repo

    async def do(self, production: ProductionPayload) -> None:
        async with self._product_repo.create_session() as session:
            product = Product(
                station_id=production.station_id,
                blueprint_efficiency=production.blueprint_efficiency
            )
            await self._product_repo.insert([product], session=session)

            # записываем транзакцию с поступлением продуктов на склад
            transaction = Transaction(
                release_date=production.release_date,
                material_id=production.product_type_id,
                product=product,
                count=production.count,
                price=production.assembly_cost,
                remains=production.count
            )
            await self._transaction_repo.insert([transaction], session=session)

            # записываем какие транзакции были использованы в качестве материалов
            await self._product_usage_repo.register_usage(product.id, production.count, session=session)
            await session.commit()
