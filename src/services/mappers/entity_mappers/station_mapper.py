from src.server.handlers.models import StationModel
from src.services.mappers.entity_mappers  import BaseEntityMapper
from src.storage.tables import Station


class StationEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = StationModel
        self._entity_type = Station
