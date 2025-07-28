from pydantic import BaseModel


class MaterialCheckerPayload(BaseModel):
    available_materials: dict[int, int]
    required_materials: dict[int, int]
