from fastapi import APIRouter

from src.server.handlers import CostCalculatorHandler


class CostCalculatorRouter:
    def __init__(self):
        self._prefix = "/api/cost_calculator"
        self._handler = CostCalculatorHandler()

        self.router = APIRouter(prefix=self._prefix, tags=[self._prefix])

        self._register_routes()

    def _register_routes(self):
        self.router.post("/")(self._handler.calculate_production_cost)
