from src.services.available_material.available_material_model import AvailableMaterialModel
from src.services.mappers.row_mappers import BaseRowMapper


class AvailableMaterialRowMapper(BaseRowMapper):
    def __init__(self):
        super().__init__()
        self._model_type = AvailableMaterialModel
