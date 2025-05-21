from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CreateOrderModel(BaseModel):
    release_date: datetime
    price: Decimal
    count: int
    tax_percent: Decimal = Field(default=7.5)
    broker_cost: Decimal = Field(default=0)
    type_id: int
