from dataclasses import dataclass
from typing import Type

from pydantic import BaseModel

from src.storage.declarative_base import DeclarativeBase


@dataclass
class MapperConfig:
    name: str
    model: Type[BaseModel]
    entity: Type[DeclarativeBase]

    def unpack(self) -> tuple:
        return self.model, self.entity
