from src.services.enetity_serice import BaseEntityService
from src.services.mappers.entity_mappers  import TypeEntityMapper
from src.storage.repositories import TypeInfoRepository


class TypeService(BaseEntityService):

    def __init__(self):
        super().__init__()
        self._main_repository = TypeInfoRepository()
        self._main_mapper = TypeEntityMapper()
