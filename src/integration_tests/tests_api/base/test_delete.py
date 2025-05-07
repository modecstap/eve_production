from abc import ABC, abstractmethod


class TestDelete(ABC):

    @abstractmethod
    async def test_delete_single(self):
        pass
