from abc import ABC, abstractmethod

from httpx import AsyncClient


class PayloadBuilder(ABC):

    def __init__(
            self,
            client: AsyncClient
    ):
        self._client = client

    @abstractmethod
    async def build_payload(self) -> dict:
        pass

    @abstractmethod
    async def build_payloads(self) -> list[dict]:
        pass

    @abstractmethod
    async def build_update_payload(self, id_: int) -> dict:
        pass

    @abstractmethod
    def build_update_payloads(self, ids_: list[int]) -> list[dict]:
        pass
