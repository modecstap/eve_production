
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    id: int | None = None
    blueprint_efficiency: Decimal = Field(default=1)
    station_id: int
