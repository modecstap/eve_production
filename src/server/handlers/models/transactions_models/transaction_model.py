from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionModel(BaseModel):
    id: int | None = None
    release_date: datetime
    count: int
    material_id: int | str
    product_id: int | str | None = None
    price: Decimal
    remains: int
