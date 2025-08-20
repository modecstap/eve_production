from pydantic import BaseModel, Field


class RequiredMaterials(BaseModel):
    materials: dict[int, int] = Field(description="ID:кол-во")
