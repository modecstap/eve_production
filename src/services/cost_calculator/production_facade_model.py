from decimal import Decimal

from pydantic import BaseModel, Field


class CostCalculatorFacadeModel(BaseModel):
    type_id: int
    count: int
    station_id: int
    blueprint_efficiency: Decimal = Field(default=1)
