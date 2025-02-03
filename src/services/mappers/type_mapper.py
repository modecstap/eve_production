from src.server.handlers.models import TypeInfoModel
from src.services.mappers import BaseMapper
from src.storage.tables import TypeInfo


class TypeMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = TypeInfoModel
        self._entity_type = TypeInfo
