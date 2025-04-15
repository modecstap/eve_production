from fastapi import APIRouter

from src.server.handlers import AvailableMaterialHandler


class AvailableMaterialsRouter:
    def __init__(self):
        self._prefix = "/api/available_materials"
        self._handler = AvailableMaterialHandler()

        self.router = APIRouter(prefix=self._prefix, tags=[self._prefix])

        self._register_routes()

    def _register_routes(self):
        self.router.post("/")(self._handler.get_all)
