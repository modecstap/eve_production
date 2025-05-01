from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import UsedTransactionMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import UsedTransactionRepository


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="used_transaction",
    )
)
class UsedTransactionService(BaseEntityService):

    def __init__(
            self,
            repository: UsedTransactionRepository = UsedTransactionRepository(),
            mapper: UsedTransactionMapper = UsedTransactionMapper()
    ):
        super().__init__(repository, mapper)
