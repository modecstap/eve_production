from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class InsertTransactionModel(BaseModel):
    release_date: datetime = Field(default=datetime.now())
    count: int
    material_id: int
    price: Decimal
    remains: int
