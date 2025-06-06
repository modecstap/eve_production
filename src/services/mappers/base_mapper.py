from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseMapper(ABC):

    @abstractmethod
    def entity_to_model(self, model: BaseModel):
        pass

    @abstractmethod
    def entities_to_models(self, models: list[BaseModel]):
        pass
