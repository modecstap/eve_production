from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers  import UsedTransactionMapper
from src.storage.repositories import UsedTransactionRepository


class UsedTransactionService(BaseEntityService):

    def __init__(self):
        super().__init__()
        self._main_repository = UsedTransactionRepository()
        self._main_mapper = UsedTransactionMapper()
