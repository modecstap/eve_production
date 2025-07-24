from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class RequiredMaterialsModel(BaseModel):
    required_materials: dict[int, int]
