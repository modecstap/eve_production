from pydantic import BaseModel


class UpdateTypeInfoModel(BaseModel):
    id: int | None = None
    name: str
    is_produced: bool
