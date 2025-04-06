from pydantic import BaseModel


class MaterialListModel(BaseModel):
    material_id: int
    type_id: int
    need_count: int
