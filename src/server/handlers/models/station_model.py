from decimal import Decimal

from pydantic import BaseModel, Field


class StationModel(BaseModel):
    id: int | None = None
    name: str
    material_efficiency: Decimal = Field(default=1)
    tax_percent: Decimal = Field(default=0)
    security_status: Decimal = Field(default=0)
