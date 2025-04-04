from decimal import Decimal

from pydantic import BaseModel


class AvailableMaterialModel(BaseModel):
    name: str
    count: int
    mean_price: Decimal
