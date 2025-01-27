from sqlalchemy import update

from src.storage.repositories.base import BaseRepository
from src.storage.tables import Material


class MaterialRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = Material
