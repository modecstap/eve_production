from sqlalchemy.ext.asyncio import AsyncSession

from src.server.handlers.models.order_models import CreateOrderModel, OrderModel, InsertOrderModel
from src.services.exceptions import NotFoundException
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.storage.repositories import BaseRepository
from src.storage.tables import Transaction, Order


class OrderCreationService:

    def __init__(
            self,
            insert_order_model: CreateOrderModel,
            session: AsyncSession,
            transaction_repository: BaseRepository = BaseRepository(Transaction),
            order_repository: BaseRepository = BaseRepository(Order),
            insert_order_mapper: BaseEntityMapper = BaseEntityMapper(InsertOrderModel, Order),
            order_mapper: BaseEntityMapper = BaseEntityMapper(OrderModel, Order)
    ):
        self._insert_order_model = insert_order_model
        self._session = session
        self._insert_order_mapper = insert_order_mapper
        self._transaction_repository = transaction_repository
        self._order_repository = order_repository
        self._order_mapper = order_mapper

    async def create_order(self) -> OrderModel:
        order_entity = self._insert_order_mapper.model_to_entity(self._insert_order_model)
        suitable_transaction = await self._prepare_transaction()
        order_entity.transaction_id = suitable_transaction.id
        order = await self._order_repository.insert([order_entity], session=self._session)
        await self._session.commit()
        return self._order_mapper.entity_to_model(order[0])

    async def _prepare_transaction(
            self
    ) -> Transaction:
        suitable_transaction = await self._find_suitable_transaction()
        await self.subtract_material_from_transaction(suitable_transaction)
        return suitable_transaction

    async def _find_suitable_transaction(
            self
    ) -> Transaction:
        transactions = await self._transaction_repository.get_entities(
            filters=[Transaction.material_id.in_(self._insert_order_model.type_id)],
            session=self._session
        )
        for transaction in transactions:
            if self._is_transaction_suitable(transaction):
                return transaction
        raise NotFoundException(self._insert_order_model.type_id)

    def _is_transaction_suitable(
            self,
            transaction: Transaction,
    ) -> bool:
        return ((transaction.remains >= self._insert_order_model.count)
                and (transaction.material_id == self._insert_order_model.type_id))

    async def subtract_material_from_transaction(self, suitable_transaction):
        suitable_transaction.remains -= self._insert_order_model.count
        await self._transaction_repository.update([suitable_transaction], session=self._session)
