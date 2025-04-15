from fastapi import APIRouter

from src.server.handlers import ProductionHandler


class ProductionsRouter:
    def __init__(self):
        self._prefix = f"/api/productions"
        self._handler = ProductionHandler()

        self.router = APIRouter(prefix=self._prefix, tags=[self._prefix])

        self._register_routes()

    def _register_routes(self):
        self.router.post("/")(self._handler.create_products)
