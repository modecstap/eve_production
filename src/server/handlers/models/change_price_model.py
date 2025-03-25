from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.server.handlers.enums import Status


class ChangePriceModel(BaseModel):
    order_id: int
    new_price: Decimal
    broker_cost: Decimal
