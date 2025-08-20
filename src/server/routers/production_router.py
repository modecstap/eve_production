from fastapi import APIRouter

from src.server.handlers.production_handler import ProductionHandler


class ProductionRouter:
    def __init__(
            self,
            prefix: str = "production",
            handler: ProductionHandler = ProductionHandler()
    ):
        self._prefix = f"/api/{prefix}"
        self._handler = handler

        self.router = APIRouter(prefix=self._prefix, tags=[prefix])

        self._register_routes()

    def _register_routes(self):
        self.router.get("/required_materials")(self._handler.get_required_materials)
        self.router.get("/materials_availability")(self._handler.get_materials_availability)
        self.router.get("/production_cost")(self._handler.get_production_cost)
        self.router.post("/make")(self._handler.make)