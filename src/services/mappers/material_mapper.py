from src.server.handlers.models import MaterialModel
from src.services.mappers import BaseMapper
from src.storage.tables import Material


class MaterialMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = MaterialModel
        self._entity_type = Material
