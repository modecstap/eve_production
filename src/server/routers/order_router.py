from fastapi import APIRouter

from src.server.handlers import OrderHandler


class OrdersRouter:
    def __init__(self):
        self._prefix = "/api/orders"
        self._handler = OrderHandler()

        self.router = APIRouter(prefix=self._prefix, tags=[self._prefix])

        self._register_routes()

    def _register_routes(self):
        self.router.put("/{id}/sell_count")(self._handler.update_sell_count)
        self.router.put("/{id}/update_price")(self._handler.update_price)
