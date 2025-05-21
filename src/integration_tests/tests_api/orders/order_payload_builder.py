from src.integration_tests.tests_api.base import PayloadBuilder
from src.integration_tests.tests_api.transactions.transactions_payload_builder import TransactionsPayloadBuilder
from src.integration_tests.tests_api.types.types_payload_builder import TypesPayloadBuilder


class OrderPayloadBuilder(PayloadBuilder):
    async def build_payload(self) -> dict:
        transaction_payload = await TransactionsPayloadBuilder(self._client).build_payload()
        response = await self._client.post("/api/transactions/", json=transaction_payload)
        transaction = response.json()

        return {
            "transaction_id": transaction["id"],
            "release_date": "2023-01-01T00:00:00",
            "price": "100500",
            "count": "600",
            "remains": "600",
            "tax_percent": "0.05",
            "broker_cost": "0.02",
            "income": 0
        }

    async def build_payloads(self) -> list[dict]:
        transactions_payload = await TransactionsPayloadBuilder(self._client).build_payloads()
        response = await self._client.post("/api/types/bulk", json=transactions_payload)
        transactions = response.json()

        return [
            {
                "transaction_id": transaction["id"],
                "release_date": "2023-01-01T00:00:00",
                "price": "100500",
                "count": "600",
                "remains": "600",
                "tax_percent": "0.05",
                "broker_cost": "0.02",
                "income": 0
            } for transaction in transactions
        ]

    async def build_update_payload(self, id_: int) -> dict:
        response = await self._client.get(f"/api/orders/{id_}")
        order = response.json()

        return {
            "id": id_,
            "transaction_id": order["transaction_id"],
            "release_date": "2023-01-01T00:00:00",
            "price": "100500",
            "count": "600",
            "remains": "500",
            "tax_percent": "0.05",
            "broker_cost": "0.02",
            "income": "60000000"
        }

    async def build_update_payloads(self, ids_: list[int]) -> list[dict]:
        orders = []
        for id_ in ids_:
            response = await self._client.get(f"/api/orders/{id_}")
            orders.append(response.json())

        return [
            {
                "id": order["id"],
                "transaction_id": order["transaction_id"],
                "release_date": "2023-01-01T00:00:00",
                "price": "100500",
                "count": "600",
                "remains": "500",
                "tax_percent": "0.05",
                "broker_cost": "0.02",
                "income": "60000000"
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
