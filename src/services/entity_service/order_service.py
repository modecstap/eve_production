from src.server.handlers.models.order_models import CreateOrderModel, SellItemModel, ChangePriceModel, OrderModel
from src.services.entity_service import BaseEntityService
from src.services.entity_service.utils.order_creation_service import OrderCreationService
from src.services.exceptions import NotEnoughMaterialsException
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import Order


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="order",
    )
)
class OrderService(BaseEntityService):

    def __init__(
            self,
            repository: BaseRepository = BaseRepository(Order),
            mapper: BaseEntityMapper = BaseEntityMapper(OrderModel, Order),
    ):
        super().__init__(repository, mapper)

    async def create_order(self, insert_order_model: CreateOrderModel) -> OrderModel:
        async with self._main_repository.create_session() as session:
            return await OrderCreationService(insert_order_model, session).create_order(insert_order_model)

    async def create_orders(self, insert_order_models: list[CreateOrderModel]) -> list[OrderModel]:
        async with self._main_repository.create_session() as session:
            return [
                await OrderCreationService(insert_order_model, session).create_order()
                for insert_order_model
                in insert_order_models
            ]

    async def update_sell_count(self, sell_count_model: SellItemModel):
        session = self._main_repository.create_session()

        order = await self._main_repository.get_entity_by_id(sell_count_model.order_id, session=session)

        if order.remains < sell_count_model.sell_count:
            raise NotEnoughMaterialsException(
                {order.transaction.material_id: sell_count_model.sell_count - order.remains}
            )

        order.remains -= sell_count_model.sell_count
        order.income += order.price * sell_count_model.sell_count

        await self._main_repository.update([order])

    async def update_price(self, change_price_model: ChangePriceModel):
        async with self._main_repository.create_session() as session:
            order = await self._main_repository.get_entity_by_id(change_price_model.order_id, session=session)

            order.price = change_price_model.new_price
            order.broker_cost += change_price_model.broker_cost

            await self._main_repository.update([order], session=session)
            await session.commit()
