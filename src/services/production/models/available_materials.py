from pydantic import BaseModel, Field

from src.services.production.models.available_material import AvailableMaterial


class AvailableMaterials(BaseModel):
    materials: dict[int, AvailableMaterial] = Field(description="ID:доступный материал")
