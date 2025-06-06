from typing import Type

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

from src.services.mappers import BaseMapper


class BaseEntityMapper(BaseMapper):
    def __init__(
            self,
            model_type: Type[BaseModel],
            entity_type: Type[DeclarativeBase]
    ):
        self._model_type: Type[BaseModel] = model_type
        self._entity_type: Type[DeclarativeBase] = entity_type

    def model_to_entity(self, model: BaseModel):
        return self._entity_type(**model.model_dump())

    def models_to_entities(self, models: list[BaseModel]):
        return [self.model_to_entity(model) for model in models]

    def entity_to_model(self, entity: DeclarativeBase) -> BaseModel:
        return self._model_type(**entity.__dict__)

    def entities_to_models(self, entities: list[DeclarativeBase]) -> list[BaseModel]:
        return [self.entity_to_model(entity) for entity in entities]
