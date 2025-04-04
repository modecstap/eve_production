from decimal import Decimal

from pydantic import BaseModel


class ChangePriceModel(BaseModel):
    order_id: int
    new_price: Decimal
    broker_cost: Decimal
