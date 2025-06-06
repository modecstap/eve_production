from src.server.handlers.models.material_list_models import MaterialListModel
from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import  BaseEntityMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import MaterialList


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="material_list",
    )
)
class MaterialListService(BaseEntityService):

    def __init__(
            self,
            repository: BaseRepository = BaseRepository(MaterialList),
            mapper: BaseEntityMapper = BaseEntityMapper(MaterialListModel, MaterialList)
    ):
        super().__init__(repository, mapper)
