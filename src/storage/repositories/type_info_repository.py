from sqlalchemy import update

from src.server.handlers.models import StatusModel
from src.storage.repositories.base import BaseRepository
from src.storage.tables import TypeInfo


class TypeInfoRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = TypeInfo
