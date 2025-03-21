from src.server.handlers.models import InsertOrderModel, StatusModel
from src.services.enetity_serice import OrderService


class OrderHandler:
    def __init__(self):
        self.order_service = OrderService()

    async def get_orders(self):
        return await self.order_service.get_models()

    async def add_order(self, order: InsertOrderModel):
        await self.order_service.add_model(order)

    async def change_order_status(self, statuses: list[StatusModel]):
        await self.order_service.update_status(statuses)
