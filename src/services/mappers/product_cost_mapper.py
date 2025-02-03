from sqlalchemy import Row

from src.server.handlers.models import AvailableProductModel
from src.services.mappers import BaseMapper


class ProductCostMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = AvailableProductModel
        self._entity_type = Row
