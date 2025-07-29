from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class CreateOrderModel(BaseModel):
    release_date: datetime
    price: Decimal
    count: int
    remains: int = None
    tax_percent: Decimal = Field(default=7.5)
    broker_cost: Decimal = Field(default=0)
    type_id: int

    @classmethod
    @field_validator("remains", mode="before")
    def set_default_remains(cls, v, info):
        if v is None:
            return info.data.get("count")
        return v