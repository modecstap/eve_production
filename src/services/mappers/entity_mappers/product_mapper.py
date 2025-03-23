from src.server.handlers.models import ProductModel
from src.services.mappers.entity_mappers  import BaseEntityMapper
from src.storage.tables import Product


class ProductEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = ProductModel
        self._entity_type = Product
