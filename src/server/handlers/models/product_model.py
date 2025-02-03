from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    id: int | None = None
    type_id: int
    order_id: int | None = None
    production_date: datetime
    blueprint_efficiency: Decimal = Field(default=1)
    station_id: int
