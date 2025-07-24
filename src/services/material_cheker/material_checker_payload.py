from decimal import Decimal

from pydantic import BaseModel, Field


class MaterialCheckerPayload(BaseModel):
    product_type_id: int
    count: int
    blueprint_efficiency: Decimal = Field(default=1)
