from abc import ABC, abstractmethod


class TestPut(ABC):

    @abstractmethod
    async def test_put_single(self):
        pass

    @abstractmethod
    async def test_put_multiple(self):
        pass
