from typing import Type

from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import TypeEntityMapper, StationEntityMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import TypeInfoRepository, StationRepository


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="type",
    )
)
class TypeService(BaseEntityService):

    def __init__(
            self,
            repository: TypeInfoRepository=TypeInfoRepository(),
            mapper: TypeEntityMapper=TypeEntityMapper()
    ):
        super().__init__(repository, mapper)
