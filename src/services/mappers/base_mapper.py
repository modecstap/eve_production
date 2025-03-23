from abc import ABC

from pydantic import BaseModel


class BaseMapper(ABC):

    def model_to_entity(self, model: BaseModel):
        pass
