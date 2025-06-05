from src.server.handlers.entity_handlers.entity_handler import EntityHandler
from src.server.handlers.models.order_models import OrderModel, ChangePriceModel, SellItemModel, \
    UpdateOrderModel, InsertOrderModel
from src.services.utils import ServiceFactory


class OrderHandler(EntityHandler):
    MODEL = OrderModel
    INSERT_MODEL = InsertOrderModel
    UPDATE_MODEL = UpdateOrderModel

    def __init__(self):
        super().__init__(ServiceFactory.get_entity_service("order"))

    async def get_all(self) -> list[MODEL]:
        return await super().get_all()

    async def get(self, id: int) -> MODEL:
        return await super().get(id)

    async def create(self, data: INSERT_MODEL) -> MODEL:
        return await super().create(data)

    async def create_bulk(self, data: list[INSERT_MODEL]) -> list[MODEL]:
        return await super().create_bulk(data)

    async def update(self, id: int, data: UPDATE_MODEL) -> MODEL:
        return await super().update(id, data)

    async def update_bulk(self, data: list[UPDATE_MODEL]) -> list[MODEL]:
        return await super().update_bulk(data)

    async def delete(self, id: int) -> dict:
        return await super().delete(id)

    async def update_sell_count(self, id: int, sell_count_model: SellItemModel):
        sell_count_model.order_id = id
        await self._service.update_sell_count(sell_count_model)

    async def update_price(self, id: int, change_price_model: ChangePriceModel):
        change_price_model.order_id = id
        await self._service.update_price(change_price_model)
