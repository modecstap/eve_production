from src.server.handlers.models import TransactionModel
from src.services.mappers.entity_mappers  import BaseEntityMapper
from src.storage.tables import Transaction


class TransactionEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = TransactionModel
        self._entity_type = Transaction
