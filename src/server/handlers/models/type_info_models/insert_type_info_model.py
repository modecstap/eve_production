from pydantic import BaseModel


class InsertTypeInfoModel(BaseModel):
    id: int
    name: str
