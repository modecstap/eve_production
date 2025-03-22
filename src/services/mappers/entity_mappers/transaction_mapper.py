from src.server.handlers.models import TransactionModel
from src.services.mappers.entity_mappers  import BaseMapper
from src.storage.tables import Transaction


class TransactionMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = TransactionModel
        self._entity_type = Transaction
