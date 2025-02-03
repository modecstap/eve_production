from src.server.handlers.models import ProductModel
from src.services.mappers import BaseMapper
from src.storage.tables import Product


class ProductMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = ProductModel
        self._entity_type = Product
