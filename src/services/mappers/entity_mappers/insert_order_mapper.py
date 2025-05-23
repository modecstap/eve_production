from src.server.handlers.models.order_models import CreateOrderModel
from src.services.mappers.entity_mappers  import BaseEntityMapper
from src.storage.tables import Order


class InsertOrderEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = CreateOrderModel
        self._entity_type = Order

    def model_to_entity(self, order: CreateOrderModel) -> Order:
        return self._entity_type(
            release_date=order.release_date,
            count=order.count,
            remains=order.count,
            price=order.price,
            tax_percent=order.tax_percent,
            broker_cost=order.broker_cost,
        )
