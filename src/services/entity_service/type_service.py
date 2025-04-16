from typing import Type

from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import TypeEntityMapper, StationEntityMapper
from src.services.utils import EntityServiceFactory, ServiceConfig
from src.storage.repositories import TypeInfoRepository, StationRepository


@EntityServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="type",
        repository=StationRepository,
        mapper=StationEntityMapper
    )
)
class TypeService(BaseEntityService):

    def __init__(self, repository: Type[TypeInfoRepository], mapper: Type[TypeEntityMapper]):
        super().__init__(repository, TypeEntityMapper)
