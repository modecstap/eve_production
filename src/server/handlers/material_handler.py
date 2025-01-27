from aiohttp.web import Request

from src.services import MaterialService


class MaterialHandler:
    def __init__(self):
        self._service = MaterialService()

    async def get_materials(self, request: Request):
        return await self._service.get_models()
