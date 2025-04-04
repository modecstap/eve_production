from decimal import Decimal

from pydantic import BaseModel


class UpdateStationModel(BaseModel):
    id: int | None = None
    name: str
    material_efficiency: Decimal
    tax_percent: Decimal
    security_status: Decimal
