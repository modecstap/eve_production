from dataclasses import dataclass
from typing import Type

from src.services.mappers.entity_mappers import BaseEntityMapper
from src.storage.repositories import BaseRepository


@dataclass
class ServiceConfig:
    name: str
    repository: Type[BaseRepository]
    mapper: Type[BaseEntityMapper]
