from src.services.entity_service import TypeService


class TypeHandler:
    def __init__(self):
        self.type_service = TypeService()

    async def get_types(self):
        return await self.type_service.get_models()
