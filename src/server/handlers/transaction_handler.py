from src.server.handlers.models import TransactionModel
from src.services.entity_service import TransactionService


class TransactionHandler:
    def __init__(self):
        self.transaction_service = TransactionService()

    async def get_transactions(self):
        return await self.transaction_service.get_models()

    async def get_available_materials(self):
        return await self.transaction_service.get_available_materials()

    async def add_transactions(self, transactions: list[TransactionModel]):
        await self.transaction_service.add_models(transactions)
