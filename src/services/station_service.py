from src.services import BaseService
from src.services.mappers import StationMapper
from src.storage.repositories import StationRepository


class StationService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = StationRepository()
        self._main_mapper = StationMapper()
