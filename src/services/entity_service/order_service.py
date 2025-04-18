from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.server.handlers.models.order_models import InsertOrderModel, SellItemModel, ChangePriceModel
from src.services.entity_service import BaseEntityService
from src.services.exceptions import NotEnoughMaterialsException
from src.services.mappers.entity_mappers import InsertOrderEntityMapper, OrderEntityMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import OrderRepository, TransactionRepository
from src.storage.tables import Transaction


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="order",
    )
)
class OrderService(BaseEntityService):

    def __init__(
            self,
            repository: OrderRepository=OrderRepository(),
            mapper: OrderEntityMapper=OrderEntityMapper(),
            transaction_repository: TransactionRepository=TransactionRepository(),
            insert_order_mapper: InsertOrderEntityMapper=InsertOrderEntityMapper()
    ):
        super().__init__(repository, mapper)
        self._transaction_repository = transaction_repository
        self._insert_order_mapper = insert_order_mapper

    async def add_model(self, insert_order_model: InsertOrderModel):
        session = self._main_repository.create_session()
        try:
            await self.__try_add_model(insert_order_model, session)
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    async def __try_add_model(self, insert_order_model: InsertOrderModel, session):
        order_entity = self._insert_order_mapper.model_to_entity(insert_order_model)
        await self.__prepare_transaction(insert_order_model, order_entity, session)
        await self._main_repository.insert([order_entity], session=session)
        await session.commit()

    async def __prepare_transaction(self, insert_order_model, order_entity, session):
        suitable_transaction = await self.__find_suitable_transaction(insert_order_model, session)
        order_entity.transaction_id = suitable_transaction.id
        await self.subtract_material_from_transaction(insert_order_model, session, suitable_transaction)

    async def subtract_material_from_transaction(self, insert_order_model, session, suitable_transaction):
        suitable_transaction.remains -= insert_order_model.count
        await self._transaction_repository.update(suitable_transaction, session=session)

    async def __find_suitable_transaction(
            self,
            insert_order_model: InsertOrderModel,
            session
    ) -> Transaction:
        transactions = await self._transaction_repository.get_transactions_by_type_id(
            [insert_order_model.type_id],
            session=session
        )

        for transaction in transactions:
            if self.__is_transaction_suitable(transaction, insert_order_model):
                return transaction

        raise NotEnoughMaterialsException()

    @staticmethod
    def __is_transaction_suitable(
            transaction: Transaction,
            insert_order_model: InsertOrderModel
    ) -> bool:
        return ((transaction.remains >= insert_order_model.count)
                and (transaction.material_id == insert_order_model.type_id))

    async def __try_add_models(self, insert_order_models):
        for insert_order_model in insert_order_models:
            await self.add_model(insert_order_model)

    async def add_models(self, insert_order_models: list[InsertOrderModel]):
        await self.__try_add_models(insert_order_models)

    async def update_sell_count(self, sell_count_model: SellItemModel):
        session = self._main_repository.create_session()

        order = await self._main_repository.get_entitiy_by_id(sell_count_model.order_id, session=session)

        if order.remains < sell_count_model.sell_count:
            raise NotEnoughMaterialsException

        order.remains -= sell_count_model.sell_count
        order.income += order.price * sell_count_model.sell_count

        await self._main_repository.update(order)

    async def update_price(self, change_price_model: ChangePriceModel):
        session = self._main_repository.create_session()
        try:
            await self.__try_update_price(change_price_model, session)
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    async def __try_update_price(self, change_price_model: ChangePriceModel, session: AsyncSession):
        order = await self._main_repository.get_entitiy_by_id(change_price_model.order_id, session=session)

        order.price = change_price_model.new_price
        order.broker_cost += change_price_model.broker_cost

        await self._main_repository.update([order], session=session)
        await session.commit()
