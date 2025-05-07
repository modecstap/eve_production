from pydantic import BaseModel


class InsertTypeInfoModel(BaseModel):
    name: str
    is_produced: bool
