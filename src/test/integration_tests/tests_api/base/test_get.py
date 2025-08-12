from abc import ABC, abstractmethod


class TestGet(ABC):

    @abstractmethod
    async def test_get_single(self):
        pass

    @abstractmethod
    async def test_get_multiple(self):
        pass
