from src.integration_tests.tests_api.base import PayloadBuilder
from src.integration_tests.tests_api.types.types_payload_builder import TypesPayloadBuilder


class OrderPayloadBuilder(PayloadBuilder):
    async def build_payload(self) -> dict:
        types_payload = await TypesPayloadBuilder(self._client).build_payload()
        response = await self._client.post("/api/types/", json=types_payload)
        type_ = response.json()

        return {
            "release_date": "2023-01-01",
            "price": "100500",
            "count": "600",
            "tax_percent": "0.05",
            "broker_cost": "0.02",
            "type_id": type_["id"]
        }

    async def build_payloads(self) -> list[dict]:
        types_payload = await TypesPayloadBuilder(self._client).build_payloads()
        response = await self._client.post("/api/types/bulk", json=types_payload)
        types = response.json()

        return [
            {
                "release_date": "2023-01-01",
                "price": "100500",
                "count": "600",
                "tax_percent": "0.05",
                "broker_cost": "0.02",
                "type_id": type_["id"]
            } for type_ in types
        ]

    async def build_update_payload(self, id_: int) -> dict:
        response = await self._client.get(f"/api/orders/{id_}")
        order = response.json()

        return {
            "id": id_,
            "release_date": "2023-01-01",
            "price": "200600",
            "count": "600",
            "tax_percent": "0.05",
            "broker_cost": "0.02",
            "type_id": order["type_id"]
        }

    async def build_update_payloads(self, ids_: list[int]) -> list[dict]:
        orders = []
        for id_ in ids_:
            response = await self._client.get(f"/api/orders/{id_}")
            orders.append(response.json())

        return [
            {
                "id": order["id"],
                "release_date": "2023-01-01",
                "price": "200600",
                "count": "600",
                "tax_percent": "0.05",
                "broker_cost": "0.02",
                "type_id": order["type_id"]
            } for order in orders
        ]

    async def build_sell_count_payload(self, id_: int) -> dict:
        return {
            "order_id": id_,
            "sell_count": "100"
        }

    async def build_update_price_payload(self, id_: int):
        return {
            "order_id": id_,
            "new_price": "70500",
            "broker_cost": "4000"
        }
