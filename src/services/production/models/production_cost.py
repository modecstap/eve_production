from decimal import Decimal

from pydantic import BaseModel, Field


class ProductionCostModel(BaseModel):
    materials_cost: dict[int, Decimal] = Field(default_factory=dict)
    production_cost: Decimal = Field(default=Decimal(0))
