from fastapi import APIRouter

from src.server.handlers import CostCalculatorHandler


class CostCalculatorRouter:
    def __init__(
            self,
            prefix: str = "cost_calculator",
            handler: CostCalculatorHandler = CostCalculatorHandler()
    ):
        self._prefix = f"/api/{prefix}"
        self._handler = handler

        self.router = APIRouter(prefix=self._prefix, tags=[prefix])

        self._register_routes()

    def _register_routes(self):
        self.router.post("/")(self._handler.calculate_production_cost)
