from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, root_validator


class CreateOrderModel(BaseModel):
    release_date: datetime
    price: Decimal
    count: int
    remains: int = None
    tax_percent: Decimal = Field(default=7.5)
    broker_cost: Decimal = Field(default=0)
    type_id: int

    @root_validator(pre=True)
    def set_remains_default(cls, values):
        if 'remains' not in values or values['remains'] is None:
            values['remains'] = values.get('count')
        return values