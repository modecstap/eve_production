from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.server.handlers.enums import Status


class InsertOrderModel(BaseModel):
    id: int | None = None
    price: Decimal
    commission_percent: Decimal = Field(default=2.35)
    tax_percent: Decimal = Field(default=4.5)
    updating_cost: Decimal = Field(default=0)
    release_date: datetime
    status: Status = Field(default=1)
    product_count: int
    type_id: int
