from src.server.handlers.entity_handlers.entity_handler import EntityHandler
from src.server.handlers.models.transactions_models import TransactionModel, InsertTransactionModel, \
    UpdateTransactionModel
from src.services.utils import ServiceFactory


class TransactionHandler(EntityHandler):

    def __init__(self):
        self._service = ServiceFactory.get_entity_service("transaction")

    async def get_all(
            self,
            replace_id_with_name: bool | None = None
    ) -> list[TransactionModel]:
        models = await self._service.get_models(replace_id_with_name)
        return models

    async def get(self, id: int) -> TransactionModel:
        return await super().get(id)

    async def create(self, data: InsertTransactionModel) -> TransactionModel:
        return await super().create(data)

    async def create_bulk(self, data: list[InsertTransactionModel]) -> list[TransactionModel]:
        return await super().create_bulk(data)

    async def update(self, id: int, data: UpdateTransactionModel) -> TransactionModel:
        return await super().update(id, data)

    async def update_bulk(self, data: list[UpdateTransactionModel]) -> list[TransactionModel]:
        return await super().update_bulk(data)

    async def delete(self, id: int) -> dict:
        return await super().delete(id)
