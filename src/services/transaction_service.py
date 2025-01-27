from src.mappers import TransactionMapper
from src.services import BaseService
from src.storage.repositories import TransactionRepository


class TransactionService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = TransactionRepository()
        self._main_mapper = TransactionMapper()
