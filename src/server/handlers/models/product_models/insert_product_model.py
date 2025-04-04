from decimal import Decimal

from pydantic import BaseModel


class InsertProductModel(BaseModel):
    blueprint_efficiency: Decimal
    station_id: int
