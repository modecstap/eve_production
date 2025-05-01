from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import MaterialListEntityMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import MaterialListRepository


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="material_list",
    )
)
class MaterialListService(BaseEntityService):

    def __init__(
            self,
            repository: MaterialListRepository = MaterialListRepository(),
            mapper: MaterialListEntityMapper = MaterialListEntityMapper()
    ):
        super().__init__(repository, mapper)
