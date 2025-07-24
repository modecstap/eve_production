from fastapi import APIRouter

from src.server.handlers import AvailableMaterialHandler


class AvailableMaterialsRouter:
    def __init__(
            self,
            prefix: str = "available_material",
            handler: AvailableMaterialHandler = AvailableMaterialHandler()
    ):
        self._prefix = f"/api/{prefix}"
        self._handler = handler

        self.router = APIRouter(prefix=self._prefix, tags=[prefix])

        self._register_routes()

    def _register_routes(self):
        self.router.post("/")(self._handler.get_all)
