from pydantic import BaseModel


class InsertMaterialListModel(BaseModel):
    material_id: int
    type_id: int
    need_count: int
