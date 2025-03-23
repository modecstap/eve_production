from src.server.handlers.models import TypeInfoModel
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.storage.tables import TypeInfo


class TypeEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = TypeInfoModel
        self._entity_type = TypeInfo
