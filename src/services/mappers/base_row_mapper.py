from abc import ABC

from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from sqlalchemy import Row


class BaseRowMapper(ABC):
    def __init__(self):
        self._model_type: BaseModel = None

    def entity_to_model(self, row: Row):
        return self._model_type(**row._mapping)

    def entities_to_models(self, rows: list[Row]):
        return [self.entity_to_model(row) for row in rows]
