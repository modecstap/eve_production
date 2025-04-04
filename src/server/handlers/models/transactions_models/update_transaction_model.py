from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class UpdateTransactionModel(BaseModel):
    id: int | None = None
    release_date: datetime
    count: int
    material_id: int
    price: Decimal
    remains: int
