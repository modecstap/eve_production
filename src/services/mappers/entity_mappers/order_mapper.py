from src.server.handlers.models import InsertOrderModel
from src.services.mappers.entity_mappers  import BaseEntityMapper
from src.storage.tables import Order


class OrderEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = InsertOrderModel
        self._entity_type = Order

    def model_to_entity(self, order: InsertOrderModel):
        return self._entity_type(
            id=order.id,
            price=order.price,
            commission_percent=order.commission_percent,
            tax_percent=order.tax_percent,
            updating_cost=order.updating_cost,
            release_date=order.release_date,
            status=order.status
        )
