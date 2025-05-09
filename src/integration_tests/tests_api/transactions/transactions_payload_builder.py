from src.integration_tests.tests_api.base import PayloadBuilder
from src.integration_tests.tests_api.types.types_payload_builder import TypesPayloadBuilder


class TransactionsPayloadBuilder(PayloadBuilder):

    async def build_payload(self) -> dict:
        types_payload = await TypesPayloadBuilder(self._client).build_payload()
        response = await self._client.post("/api/types/", json=types_payload)
        type_ = response.json()

        return {
            "material_id": type_["id"],
            "product_id": None,
            "release_date": "2025-01-01T00:00:00",
            "count": 5000,
            "price": "1300.5",
            "remains": 4000,
        }

    async def build_payloads(self) -> list[dict]:
        types_payloads = await TypesPayloadBuilder(self._client).build_payloads()
        response = await self._client.post("/api/types/bulk", json=types_payloads)
        types = response.json()

        return [
            {
                "material_id": type_["id"],
                "product_id": None,
                "release_date": "2025-01-01T00:00:00",
                "count": 5000,
                "price": "1300.5",
                "remains": 4000,
            } for type_ in types
        ]

    async def build_update_payload(self, id_) -> dict:
        response = await self._client.get(f"/api/transactions/{id_}")
        transaction = response.json()

        return {
            "id": id_,
            "material_id": transaction["material_id"],
            "product_id": None,
            "release_date": "2025-01-01T00:00:00",
            "count": 5000,
            "price": "1000.5",
            "remains": 4000,
        }

    async def build_update_payloads(self, ids_) -> list[dict]:
        response = await self._client.get(f"/api/transactions/")
        transactions = response.json()

        return [{
            "id": transaction["id"],
            "material_id": transaction["material_id"],
            "product_id": None,
            "release_date": "2025-01-01T00:00:00",
            "count": 5000,
            "price": "1000.5",
            "remains": 4000,
        } for transaction in transactions]
