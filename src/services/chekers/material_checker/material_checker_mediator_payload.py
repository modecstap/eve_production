from pydantic import BaseModel


class MaterialCheckerMediatorPayload(BaseModel):
    required_materials: dict[int, int]
