from typing import Any, Sequence

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession

from src.server import FastAPIServer
from src.server.handlers.models import StationModel
from src.storage import Database
from src.storage.tables import Station
from src.tests.tests_api.abstract_test_api import AbstractTestApi


class TestStationApi(AbstractTestApi):
    model: StationModel = StationModel
    entity: Station = Station
    db = Database()
    client = TestClient(FastAPIServer().app)

    async def setup_db(self):
        self.db.create_connection()
        try:
            await self.db.drop_all()
            await self.db.create_all()
        finally:
            await self.db.dispose_connection()

    async def insert_into_db(self, entities: list):
        self.db.create_connection()
        async with self.db.async_session_maker() as session:
            session.add_all(entities)
            await session.commit()
            await session.flush()
        await self.db.dispose_connection()

    async def get_from_db(self, entity_type, ids: list[int]) -> Sequence[Row[Any]]:
        self.db.create_connection()
        async with self.db.async_session_maker() as session:
            session: AsyncSession
            result = await session.execute(
                select(entity_type)
                .where(entity_type.id.in_(ids))
            )
            entities = result.scalars().all()
        await self.db.dispose_connection()
        return entities

    @pytest.mark.asyncio
    async def test_get_positive(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        station = Station(name="test station", material_efficiency=1, tax_percent=0.025, security_status=1)
        await self.insert_into_db([station])

        station_dict = StationModel(**station.__dict__).model_dump()

        # ОПЕРАЦИИ
        response = self.client.get(f"/stations/{station.id}")
        data = response.json()

        # ПРОВЕРКИ
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert data == station_dict, f"Expected id {station_dict}, got {data}"

    @pytest.mark.asyncio
    async def test_get_negative(self):
        # ПОСТРОЕНИЕ

        # ОПЕРАЦИИ
        response = self.client.get(f"/stations/{999999}")
        data = response.json()

        # ПРОВЕРКИ
        assert response.status_code == 404, \
            f"Expected 404, got {response.status_code}"

    @pytest.mark.asyncio
    async def test_gets_positive(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        stations = [
            Station(name="Station 1", material_efficiency=0.1, tax_percent=0.05, security_status=0.9),
            Station(name="Station 2", material_efficiency=0.2, tax_percent=0.03, security_status=0.7),
        ]
        await self.insert_into_db(stations)

        station_dict = [
            StationModel(**station.__dict__).model_dump() for station in stations
        ]

        # ОПЕРАЦИИ
        response = self.client.get("/stations/")
        data = response.json()

        # ПРОВЕРКИ
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
        assert data == station_dict, \
            f"Expected id {station_dict}, got {data}"

    @pytest.mark.asyncio
    async def test_insert_positive(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        payload = {"name": "New Station", "material_efficiency": 0.15, "tax_percent": 3.5, "security_status": 0.8}

        # ОПЕРАЦИИ
        response = self.client.post("/stations/", json=payload)
        data = response.json()

        # ПРОВЕРКИ
        assert "id" in data, \
            "ID not in response"
        assert data["name"] == payload["name"], \
            f"Expected name {payload['name']}, got {data['name']}"
        assert data["material_efficiency"] == payload["material_efficiency"], \
            f"Expected material_efficiency {payload['material_efficiency']}, got {data['material_efficiency']}"
        assert data["tax_percent"] == payload["tax_percent"], \
            f"Expected tax_percent {payload['tax_percent']}, got {data['tax_percent']}"
        assert data["security_status"] == payload["security_status"], \
            f"Expected security_status {payload['security_status']}, got {data['security_status']}"

    @pytest.mark.asyncio
    async def test_insert_negative(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        payload = {"material_efficiency": "asbc", "tax_percent": "asd", "security_status": -200}

        # ОПЕРАЦИИ
        response = self.client.post("/stations/", json=payload)

        # ПРОВЕРКИ
        assert response.status_code == 400, \
            f"Expected 400, got {response.status_code}"

    @pytest.mark.asyncio
    async def test_inserts_positive(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        payload = [
            {"name": "New Station", "material_efficiency": 0.15, "tax_percent": 3.5, "security_status": 0.8},
            {"name": "New Station1", "material_efficiency": 0.1, "tax_percent": 3, "security_status": 1},
        ]

        # ОПЕРАЦИИ
        response = self.client.post("/stations/", json=payload)
        data = response.json()

        # ПРОВЕРКИ
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        for item, result in zip(payload, data):
            assert "id" in result, \
                "ID not in response"
            assert item["name"] == result["name"], \
                f"Expected name {item['name']}, got {result['name']}"
            assert item["material_efficiency"] == result["material_efficiency"], \
                f"Expected material_efficiency {item['material_efficiency']}, got {result['material_efficiency']}"
            assert item["tax_percent"] == result["tax_percent"], \
                f"Expected tax_percent {item['tax_percent']}, got {result['tax_percent']}"
            assert item["security_status"] == result["security_status"], \
                f"Expected security_status {item['security_status']}, got {result['security_status']}"

    @pytest.mark.asyncio
    async def test_inserts_negative(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        payload = [
            {"material_efficiency": "asbc", "tax_percent": "asd", "security_status": -200},
            {"name": "New Station1", "material_efficiency": 0.1, "tax_percent": 3, "security_status": 1},
        ]

        # ОПЕРАЦИИ
        response = self.client.post("/stations/", json=payload)

        # ПРОВЕРКИ
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    @pytest.mark.asyncio
    async def test_update_positive(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        station = Station(name="Station 1", material_efficiency=0.1, tax_percent=0.05, security_status=0.9)
        await self.insert_into_db([station])

        payload = {"name": "Updated Station", "material_efficiency": 0.25, "tax_percent": 7.5, "security_status": 0.95}

        # ОПЕРАЦИИ
        response = self.client.put(f"/stations/{station.id}", json=payload)
        data = response.json()

        # ПРОВЕРКИ
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
        assert data["id"] == station.id, \
            f"Expected id {station.id}, got {data['id']}"
        assert data["name"] == payload["name"], \
            f"Expected name {payload['name']}, got {data['name']}"
        assert data["material_efficiency"] == payload["material_efficiency"], \
            f"Expected material_efficiency {payload['material_efficiency']}, got {data['material_efficiency']}"
        assert data["tax_percent"] == payload["tax_percent"], \
            f"Expected tax_percent {payload['tax_percent']}, got {data['tax_percent']}"
        assert data["security_status"] == payload["security_status"], \
            f"Expected security_status {payload['security_status']}, got {data['security_status']}"

    @pytest.mark.asyncio
    async def test_updates_positive(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        stations = [
            Station(name="Station 1", material_efficiency=0.1, tax_percent=0.05, security_status=0.9),
            Station(name="Station 2", material_efficiency=0.2, tax_percent=0.03, security_status=0.7),
        ]
        await self.insert_into_db(stations)

        payloads = [
            {"name": "Updated Station 1", "material_efficiency": 0.3, "tax_percent": 12.0, "security_status": 0.95},
            {"name": "Updated Station 2", "material_efficiency": 0.4, "tax_percent": 15.0, "security_status": 1.0}
        ]

        # ОПЕРАЦИИ
        for station, payload in zip(stations, payloads):
            response = self.client.put(f"/stations/{station.id}", json=payload)
            data = response.json()

            # ПРОВЕРКИ
            assert response.status_code == 200, \
                f"Expected 200, got {response.status_code}"
            assert data["name"] == payload["name"], \
                f"Expected name {payload['name']}, got {data['name']}"
            assert data["material_efficiency"] == payload["material_efficiency"], \
                f"Expected material_efficiency {payload['material_efficiency']}, got {data['material_efficiency']}"
            assert data["tax_percent"] == payload["tax_percent"], \
                f"Expected tax_percent {payload['tax_percent']}, got {data['tax_percent']}"
            assert data["security_status"] == payload["security_status"], \
                f"Expected security_status {payload['security_status']}, got {data['security_status']}"

    @pytest.mark.asyncio
    async def test_delete_positive(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        station = self.entity(name="Station to Delete", material_efficiency=0.3, tax_percent=5.0, security_status=0.85)
        await self.insert_into_db([station])

        # ОПЕРАЦИИ
        response = self.client.delete(f"/stations/{station.id}")
        stations_after_delete = await self.get_from_db(self.entity, [station.id])
        response_after_delete = self.client.get(f"/stations/{station.id}")

        # ПРОВЕРКИ
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
        assert len(stations_after_delete) == 0, \
            "Station should be deleted from database"
        assert response_after_delete.status_code == 404, \
            f"Expected 404 after deletion, got {response_after_delete.status_code}"

    @pytest.mark.asyncio
    async def test_deletes_positive(self):
        # ПОСТРОЕНИЕ
        await self.setup_db()
        stations = [
            Station(name="Station 1", material_efficiency=0.1, tax_percent=0.05, security_status=0.9),
            Station(name="Station 2", material_efficiency=0.2, tax_percent=0.03, security_status=0.7),
        ]
        await self.insert_into_db(stations)

        # ОПЕРАЦИИ
        for station in stations:
            response = self.client.delete(f"/stations/{station.id}")
            response_after_delete = self.client.get(f"/stations/{station.id}")

            # ПРОВЕРКИ
            assert response.status_code == 200, \
                f"Expected 200, got {response.status_code}"
            assert response_after_delete.status_code == 404, \
                f"Expected 404 after deletion, got {response_after_delete.status_code}"
