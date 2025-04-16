from typing import Type

from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import MaterialListEntityMapper
from src.services.utils import EntityServiceFactory, ServiceConfig
from src.storage.repositories import MaterialListRepository


@EntityServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="material_list",
        repository=MaterialListRepository,
        mapper=MaterialListEntityMapper
    )
)
class MaterialListService(BaseEntityService):

    def __init__(self, repository: Type[MaterialListRepository], mapper: Type[MaterialListEntityMapper]):
        super().__init__(repository, mapper)
