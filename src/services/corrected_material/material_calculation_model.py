from decimal import Decimal

from pydantic import BaseModel


class MaterialCalculationModel(BaseModel):
    material_count: int
    blueprint_efficiency: Decimal
    material_efficiency: Decimal
    product_count: int
