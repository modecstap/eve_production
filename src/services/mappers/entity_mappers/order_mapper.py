from src.server.handlers.models import OrderModel
from src.services.mappers.entity_mappers  import BaseEntityMapper
from src.storage.tables import Order


class OrderEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = OrderModel
        self._entity_type = Order
