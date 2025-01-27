from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class MaterialModel(BaseModel):
    id: int | None = None
    name: str
