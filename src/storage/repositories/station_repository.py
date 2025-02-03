from src.storage.repositories.base import BaseRepository
from src.storage.tables import Station


class StationRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Station
