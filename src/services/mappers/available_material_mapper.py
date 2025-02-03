from sqlalchemy import Row

from src.server.handlers.models import AvailableMaterialModel
from src.services.mappers import BaseMapper


class AvailableMaterialMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = AvailableMaterialModel
        self._entity_type = Row
