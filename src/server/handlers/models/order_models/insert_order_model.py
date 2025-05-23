from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class InsertOrderModel(BaseModel):
    transaction_id: int
    release_date: datetime
    price: Decimal
    count: int
    remains: int
    broker_cost: Decimal = Field(default=0)
    tax_percent: Decimal = Field(default=7.5)
    income: Decimal
