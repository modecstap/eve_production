from pydantic import BaseModel


class UpdateMaterialListModel(BaseModel):
    material_id: int
    type_id: int
    need_count: int
