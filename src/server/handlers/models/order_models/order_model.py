from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.server.handlers.enums import Status


class OrderModel(BaseModel):
    id: int | None = None
    transaction_id: int
    release_date: datetime
    price: Decimal
    count: int
    remains: int
    broker_cost: Decimal = Field(default=0)
    tax_percent: Decimal = Field(default=7.5)
    income : Decimal
