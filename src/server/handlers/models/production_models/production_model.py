from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductionModel(BaseModel):
    type_id: int
    release_date: datetime
    count: int
    station_id: int
    blueprint_efficiency: Decimal = Field(default=1)
