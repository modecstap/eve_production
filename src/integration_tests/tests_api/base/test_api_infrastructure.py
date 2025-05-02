from abc import ABC, abstractmethod
from typing import Any, Type

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from src.config import Settings
from src.server import FastAPIServer
from src.storage import Database


class TestApiInfrastructure(ABC):
    model: Type[Any]
    entity: Type[Any]

    db = Database()
    client = TestClient(FastAPIServer(Settings().config.server_config).app)

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

    def to_dict(self, instance: Any) -> dict:
        return self.model(**instance.__dict__).model_dump(mode="json")

    def assert_equal(self, actual: dict, expected: dict):
        filtered_actual = {k: v for k, v in actual.items() if k in expected}
        assert filtered_actual == expected, f"Expected {expected}, got {actual}"

    # ---------- Требуемые абстрактные методы ----------

    @abstractmethod
    def build_valid_payload(self) -> dict:
        pass

    @abstractmethod
    def build_invalid_payload(self) -> dict:
        pass

    @abstractmethod
    def update_payload(self, obj_id: int) -> dict:
        pass
