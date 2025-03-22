from src.server.handlers.models import StationModel
from src.services.mappers.entity_mappers  import BaseMapper
from src.storage.tables import Station


class StationMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = StationModel
        self._entity_type = Station
