from src.server.handlers.models.order_models import InsertOrderModel, ChangePriceModel, SellItemModel
from src.server.handlers.models.order_models.order_model import OrderModel
from src.services.entity_service import OrderService


class OrderHandler:
    def __init__(self):
        self.order_service = OrderService()

    async def get_orders(self) -> OrderModel:
        return await self.order_service.get_models()

    async def add_order(self, order: InsertOrderModel):
        await self.order_service.add_model(order)

    async def update_sell_count(self, sell_count_model: SellItemModel):
        await self.order_service.update_sell_count(sell_count_model)

    async def update_price(self, change_price_model: ChangePriceModel):
        await self.order_service.update_price(change_price_model)
