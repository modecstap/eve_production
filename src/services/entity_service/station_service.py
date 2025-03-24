from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers  import StationEntityMapper
from src.storage.repositories import StationRepository


class StationService(BaseEntityService):

    def __init__(self):
        super().__init__()
        self._main_repository = StationRepository()
        self._main_mapper = StationEntityMapper()
