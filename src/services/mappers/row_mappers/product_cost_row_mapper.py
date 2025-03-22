from sqlalchemy import Row

from src.server.handlers.models import AvailableProductModel
from src.services.mappers.row_mappers import BaseRowMapper


class ProductCostRowMapper(BaseRowMapper):
    def __init__(self):
        super().__init__()
        self._model_type = AvailableProductModel
