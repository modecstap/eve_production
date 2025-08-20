from pydantic import BaseModel


class CheckResponse(BaseModel):
    possible_to_produce: bool