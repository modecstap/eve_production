from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers  import MaterialListEntityMapper
from src.storage.repositories import MaterialListRepository

class MaterialListService(BaseEntityService):

    def __init__(self):
        super().__init__()
        self._main_repository = MaterialListRepository()
        self._main_mapper = MaterialListEntityMapper()
