from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class AvailableProductModel(BaseModel):
    name: str
    production_date: datetime
    product_cost: Decimal
