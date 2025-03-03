from aiohttp.web import Request

from src.services import TypeService


class TypeHandler:
    def __init__(self):
        self.type_service = TypeService()

    async def get_types(self, request: Request):
        return await self.type_service.get_models()
