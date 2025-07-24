from abc import ABC, abstractmethod

from pydantic import BaseModel


class Service(ABC):

    @abstractmethod
    async def do(self, model: list[BaseModel] | BaseModel | None) -> list[BaseModel] | BaseModel:
        pass
