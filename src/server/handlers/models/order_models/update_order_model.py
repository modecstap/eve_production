from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class UpdateOrderModel(BaseModel):
    id: int | None = None
    transaction_id: int
    release_date: datetime
    price: Decimal
    count: int
    remains: int
    broker_cost: Decimal
    tax_percent: Decimal
    income: Decimal
