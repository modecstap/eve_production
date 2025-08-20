from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductionPayload(BaseModel):
    product_type_id: int
    release_date: datetime
    count: int
    station_id: int
    assembly_cost: Decimal = Field(description='Суммарная стоимость производства продукции')
    blueprint_efficiency: Decimal = Field(default=1)
