from abc import ABC

import pytest
from httpx import AsyncClient, ASGITransport

from src.config import Settings
from src.server import FastAPIServer
from src.storage import Database


class TestApiInfrastructure(ABC):
    db = Database()
    client: AsyncClient

    @pytest.fixture(scope="function", autouse=True)
    async def setup_db(self):
        self.db.create_connection()
        try:
            await self.db.drop_all()
            await self.db.create_all()
        except Exception as e:
            await self.db.create_all()
        finally:
            await self.db.dispose_connection()

    @pytest.fixture(autouse=True, scope="function")
    async def setup_client(self):
        app = FastAPIServer(Settings().config.server_config).app
        async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            self.client = ac
            yield

    def assert_equal(self, actual: dict, expected: dict):
        filtered_actual = {k: v for k, v in actual.items() if k in expected}
        assert filtered_actual == expected, f"Expected {expected}, got {actual}"
