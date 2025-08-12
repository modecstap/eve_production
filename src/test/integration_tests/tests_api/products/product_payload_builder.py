from src.test.integration_tests.tests_api.base import PayloadBuilder
from src.test.integration_tests.tests_api.stations.stations_payload_builder import StationsPayloadBuilder


class ProductPayloadBuilder(PayloadBuilder):
    async def build_payload(self) -> dict:
        station_payload = await StationsPayloadBuilder(self._client).build_payload()
        response = await self._client.post("/api/stations/", json=station_payload)
        station = response.json()

        return {
            "station_id": station["id"],
            "blueprint_efficiency": "0.95"
        }

    async def build_payloads(self) -> list[dict]:
        station_payloads = await StationsPayloadBuilder(self._client).build_payloads()
        response = await self._client.post("/api/stations/bulk", json=station_payloads)
        stations = response.json()
        return [
            {
                "station_id": station["id"],
                "blueprint_efficiency": "0.95"
            } for station in stations
        ]

    async def build_update_payload(self, id_: int) -> dict:
        response = await self._client.get(f"/api/products/{id_}")
        stations_id = response.json()["station_id"]
        return {
            "id": id_,
            "station_id": stations_id,
            "blueprint_efficiency": "0.95",
        }

    async def build_update_payloads(self, ids_: list[int]) -> list[dict]:
        stations_id = {}
        for id_ in ids_:
            response = await self._client.get(f"/api/products/{ids_[0]}")
            stations_id[id_] = (response.json()["station_id"])
        return [
            {
                "id": id_,
                "station_id": station_id,
                "blueprint_efficiency": "0.95",
            } for id_, station_id in stations_id.items()
        ]
