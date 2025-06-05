from src.server.handlers.models.used_transactions import UsedTransactionModel
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.storage.tables import UsedTransactionList


class UsedTransactionMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = UsedTransactionModel
        self._entity_type = UsedTransactionList
