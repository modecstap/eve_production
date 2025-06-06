from src.server.handlers.models.type_info_models import TypeInfoModel
from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import BaseEntityMapper
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
            mapper: BaseEntityMapper = BaseEntityMapper(TypeInfoModel, TypeInfo)
    ):
        super().__init__(repository, mapper)
