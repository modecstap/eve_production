from src.services import MaterialService


class MaterialHandler:
    def __init__(self):
        self._service = MaterialService()

    async def get_materials(self):
        return await self._service.get_models()
