from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductionCostPayload(BaseModel):
    production_cost: Decimal
    type_id: int
    release_date: datetime
    count: int
    station_id: int
    blueprint_efficiency: Decimal = Field(default=1)
