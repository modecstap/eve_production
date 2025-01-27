from aiohttp.web_request import Request

from src.server.handlers.models import InsertOrderModel, StatusModel
from src.services import OrderService


class OrderHandler:
    def __init__(self):
        self.order_service = OrderService()

    async def get_orders(self, request: Request):
        return await self.order_service.get_models()

    async def add_order(self, request: Request, order: InsertOrderModel):
        await self.order_service.add_model(order)

    async def change_order_status(self, request: Request, statuses: list[StatusModel]):
        await self.order_service.update_status(statuses)
