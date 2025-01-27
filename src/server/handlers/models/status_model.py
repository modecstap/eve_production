from pydantic import BaseModel

from src.server.handlers.enums import Status


class StatusModel(BaseModel):
    order_id: int
    status: Status
