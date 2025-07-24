from decimal import Decimal

from pydantic import BaseModel


class ProductionMaterialsPayload(BaseModel):
    materials: dict[int, int]
    blueprint_efficiency: Decimal
    station_material_efficiency: Decimal
    product_count: int
