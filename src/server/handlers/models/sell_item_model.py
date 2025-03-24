from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from src.server.handlers.enums import Status


class SellItemModel(BaseModel):
    order_id: int
    sell_count: Decimal
