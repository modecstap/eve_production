from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import StationEntityMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import  BaseRepository
from src.storage.tables import Station


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="station",
    )
)
class StationService(BaseEntityService):

    def __init__(
            self,
            repository: BaseRepository = BaseRepository(Station),
            mapper: StationEntityMapper = StationEntityMapper()
    ):
        super().__init__(repository, mapper)
