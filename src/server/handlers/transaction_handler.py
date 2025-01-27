from aiohttp.web import Request

from src.server.handlers.models import TransactionModel
from src.services import TransactionService


class TransactionHandler:
    def __init__(self):
        self.transaction_service = TransactionService()

    async def get_transactions(self, request: Request):
        return await self.transaction_service.get_models()

    async def add_transactions(self, request: Request, transactions: list[TransactionModel]):
        await self.transaction_service.add_models(transactions)
