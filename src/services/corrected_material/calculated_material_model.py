from pydantic import BaseModel


class CalculatedMaterialModel(BaseModel):
    calculated_material: int
