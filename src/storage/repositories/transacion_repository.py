from src.storage.repositories.base import BaseRepository
from src.storage.tables import Transaction


class TransactionRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Transaction
