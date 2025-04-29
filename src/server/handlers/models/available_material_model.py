from decimal import Decimal

from pydantic import BaseModel


class AvailableMaterialModel(BaseModel):
    material_id: int
    name: str
    count: int
    mean_price: Decimal
