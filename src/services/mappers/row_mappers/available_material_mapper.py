from sqlalchemy import Row

from src.server.handlers.models import AvailableMaterialModel
from src.services.mappers.row_mappers import BaseRowMapper


class AvailableMaterialRowMapper(BaseRowMapper):
    def __init__(self):
        super().__init__()
        self._model_type = AvailableMaterialModel
