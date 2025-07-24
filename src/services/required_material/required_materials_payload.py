from decimal import Decimal

from pydantic import BaseModel, Field


class RequiredMaterialsPayload(BaseModel):
    product_type_id: int
    count: int
    blueprint_efficiency: Decimal = Field(default=1)
