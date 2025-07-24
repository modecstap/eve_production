from pydantic import BaseModel


class ProductionMaterials(BaseModel):
    required_materials: dict[int, int]
