from pydantic import BaseModel


class RequiredMaterialsModel(BaseModel):
    required_materials: dict[int, int]
