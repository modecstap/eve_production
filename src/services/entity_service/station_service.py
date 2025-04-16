from typing import Type

from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import StationEntityMapper
from src.services.utils import EntityServiceFactory, ServiceConfig
from src.storage.repositories import StationRepository


@EntityServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="station",
        repository=StationRepository,
        mapper=StationEntityMapper
    )
)
class StationService(BaseEntityService):

    def __init__(self, repository: Type[StationRepository], mapper: Type[StationEntityMapper]):
        super().__init__(repository, mapper)
