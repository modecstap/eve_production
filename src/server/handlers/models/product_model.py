from datetime import datetime

from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int | None = None
    type_id: int | None = None
    order_id: int | None = None
    production_date: datetime
