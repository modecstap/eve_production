from decimal import Decimal

from pydantic import BaseModel


class SellItemModel(BaseModel):
    order_id: int
    sell_count: Decimal
