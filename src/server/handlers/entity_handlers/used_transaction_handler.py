from src.server.handlers.entity_handlers.entity_handler import EntityHandler
from src.server.handlers.models.used_transactions import UsedTransactionModel, InsertUsedTransactionModel, \
    UpdateUsedTransactionModel
from src.services.utils import EntityServiceFactory


class UsedTransactionHandler(EntityHandler):
    MODEL = UsedTransactionModel
    INSERT_MODEL = InsertUsedTransactionModel
    UPDATE_MODEL = UpdateUsedTransactionModel

    def __init__(self):
        super().__init__(EntityServiceFactory.get_entity_service("used_transaction"))

    async def get_all(self) -> list[MODEL]:
        return await super().get_all()

    async def get(self, id: int) -> MODEL:
        return await super().get(id)

    async def create(self, data: INSERT_MODEL) -> MODEL:
        return await super().create(data)

    async def create_bulk(self, data: list[INSERT_MODEL]) -> list[MODEL]:
        return await super().create_bulk(data)

    async def update(self, id: int, data: UPDATE_MODEL) -> MODEL:
        return await super().update(id, data)

    async def update_bulk(self, data: list[UPDATE_MODEL]) -> list[MODEL]:
        return await super().update_bulk(data)

    async def delete(self, id: int) -> dict:
        return await super().delete(id)
