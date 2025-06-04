from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import TypeEntityMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import TypeInfo


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="type",
    )
)
class TypeService(BaseEntityService):

    def __init__(
            self,
            repository: BaseRepository = BaseRepository(TypeInfo),
            mapper: TypeEntityMapper = TypeEntityMapper()
    ):
        super().__init__(repository, mapper)
