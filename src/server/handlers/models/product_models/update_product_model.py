from decimal import Decimal

from pydantic import BaseModel


class UpdateProductModel(BaseModel):
    id: int | None = None
    blueprint_efficiency: Decimal
    station_id: int
