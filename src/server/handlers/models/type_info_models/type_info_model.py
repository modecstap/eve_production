from pydantic import BaseModel


class TypeInfoModel(BaseModel):
    id: int | None = None
    name: str
