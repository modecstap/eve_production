from abc import ABC

from pydantic import BaseModel
from sqlalchemy.orm import declarative_base

from src.storage.tables import Order


class BaseMapper(ABC):
    def __init__(self):
        self._model_type: BaseModel = None
        self._entity_type: Order = None

    def model_to_entity(self, model: BaseModel):
        return self._entity_type(**model.dict())

    def models_to_entities(self, models: list[BaseModel]):
        return [self.model_to_entity(model) for model in models]

    def entity_to_model(self, entity: declarative_base):
        return self._model_type(**entity.__dict__)

    def entities_to_models(self, entities: list[declarative_base]):
        return [self.entity_to_model(entity) for entity in entities]
