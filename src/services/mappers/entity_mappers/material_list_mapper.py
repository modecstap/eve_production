from src.server.handlers.models.material_list_models import MaterialListModel
from src.services.mappers.entity_mappers  import BaseEntityMapper
from src.storage.tables import  MaterialList


class MaterialListEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = MaterialListModel
        self._entity_type = MaterialList
