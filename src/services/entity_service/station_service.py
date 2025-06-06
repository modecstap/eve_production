from src.server.handlers.models.station_models import StationModel
from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
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
            mapper: BaseEntityMapper = BaseEntityMapper(StationModel, Station)
    ):
        super().__init__(repository, mapper)
