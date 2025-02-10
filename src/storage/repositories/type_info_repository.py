from src.storage.repositories.base import BaseRepository
from sqlalchemy import select
from src.storage.tables import TypeInfo, MaterialList


class TypeInfoRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self._entity = TypeInfo
