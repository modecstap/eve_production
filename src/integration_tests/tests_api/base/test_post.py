from abc import ABC, abstractmethod


class TestPost(ABC):

    @abstractmethod
    async def test_post_single(self):
        pass

    @abstractmethod
    async def test_post_multiple(self):
        pass
