from typing import Type

from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import UsedTransactionMapper
from src.services.utils import EntityServiceFactory, ServiceConfig
from src.storage.repositories import UsedTransactionRepository


@EntityServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="used_transaction",
        repository=UsedTransactionRepository,
        mapper=UsedTransactionMapper
    )
)
class UsedTransactionService(BaseEntityService):

    def __init__(self, repository: Type[UsedTransactionRepository], mapper: Type[UsedTransactionMapper]):
        super().__init__(repository, mapper)
