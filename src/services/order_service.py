from src.server.handlers.models import StatusModel, InsertOrderModel
from src.services import BaseService
from src.services.exceptions import ProductCountException
from src.services.mappers import OrderMapper
from src.storage.repositories import ProductRepository, OrderRepository


class OrderService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = OrderRepository()
        self._product_repository = ProductRepository()
        self._main_mapper = OrderMapper()

    async def add_model(self, insert_order_model: InsertOrderModel):
        try:
            await self.__try_add_model(insert_order_model)
        except Exception as e:
            await self._main_repository.rollback_transaction()
        finally:
            await self._main_repository.close_transaction()

    async def __try_add_model(self, insert_order_model):
        await self._main_repository.start_transaction()
        order_entity = self._main_mapper.model_to_entity(insert_order_model)
        inserted_order_entity = (await self._main_repository.insert([order_entity]))[0]
        products = await self._product_repository.get_products_without_order_by_type(insert_order_model.type_id)
        if len(products) < insert_order_model.product_count:
            raise ProductCountException()
        for i in range(insert_order_model.product_count):
            products[i].order = inserted_order_entity
        await self._product_repository.insert(products)

    async def add_models(self, insert_order_models: list[InsertOrderModel]):
        try:
            await self.__try_add_models(insert_order_models)
        except Exception as e:
            await self._main_repository.rollback_transaction()
        finally:
            await self._main_repository.close_transaction()

    async def __try_add_models(self, insert_order_models):
        await self._main_repository.start_transaction()
        for insert_order_model in insert_order_models:
            await self.add_model(insert_order_model)

    async def update_status(self, statuses: list[StatusModel]):
        try:
            await self.__try_update_statuses(statuses)
        except Exception as e:
            await self._main_repository.rollback_transaction()
        finally:
            await self._main_repository.close_transaction()


    async def __try_update_statuses(self, statuses):
        await self._main_repository.start_transaction()
        await self._main_repository.update_statuses(statuses)
