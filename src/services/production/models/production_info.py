from decimal import Decimal

from pydantic import BaseModel, Field


class ProductionInfo(BaseModel):
    product_type_id: int
    count: int
    blueprint_efficiency: Decimal = Field(default=1)
    material_efficiency: Decimal = Field(default=1)
    station_id: int
    assembly_cost: Decimal = Field(
        description='Суммарная стоимость производства продукции (налог станции)',
        default=0,
    )
