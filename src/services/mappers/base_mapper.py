from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseMapper(ABC):

    @abstractmethod
    def model_to_entity(self, model: BaseModel):
        pass
