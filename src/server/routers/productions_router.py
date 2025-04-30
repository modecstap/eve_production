from fastapi import APIRouter

from src.server.handlers import ProductionHandler


class ProductionsRouter:
    def __init__(
            self,
            prefix: str = "productions",
            handler: ProductionHandler = ProductionHandler()
    ):
        self._prefix = f"/api/{prefix}"
        self._handler = handler

        self.router = APIRouter(prefix=self._prefix, tags=[prefix])

    def _register_routes(self):
        self.router.post("/")(self._handler.create_products)
