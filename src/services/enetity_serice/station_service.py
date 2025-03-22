from src.services.enetity_serice import BaseEntityService
from src.services.mappers.entity_mappers  import StationMapper
from src.storage.repositories import StationRepository


class StationService(BaseEntityService):

    def __init__(self):
        super().__init__()
        self._main_repository = StationRepository()
        self._main_mapper = StationMapper()
