from src.integration_tests.tests_api.base import BaseTestApi
from src.integration_tests.tests_api.orders.order_payload_builder import OrderPayloadBuilder


class TestOrdersApi(BaseTestApi):
    api_version = "api"
    endpoint = "orders"
    payload_builder = OrderPayloadBuilder

    async def test_put_sell_count(self):
        # Arrange
        payload = await self.payload_builder.build_payload()
        post_response = await self.client.post(f"/{self.api_version}/{self.endpoint}/", json=payload)
        obj_id = post_response.json()["id"]
        sell_count = await self.payload_builder.build_sell_count_payload(obj_id)

        # Act
        put_response = await self.client.put(
            f"/{self.api_version}/{self.endpoint}/{obj_id}/sell_count",
            json=sell_count
        )

        # Assert
        assert put_response.status_code == 200, f" 200 but got {put_response.status_code}"
        # TODO: проверить обновляется ли транзакция на которую ссылается order.
        # TODO: проверить сам order.

    async def test_put_update_price(self):
        # Arrange
        payload = await self.payload_builder.build_payload()
        post_response = await self.client.post(f"/{self.api_version}/{self.endpoint}/", json=payload)
        obj_id = post_response.json()["id"]
        sell_count = await self.payload_builder.build_update_price_payload(obj_id)

        # Act
        put_response = await self.client.put(
            f"/{self.api_version}/{self.endpoint}/{obj_id}/update_price",
            json=sell_count
        )

        # Assert
        assert put_response.status_code == 200, f" 200 but got {put_response.status_code}"
        # TODO: проверить обновляется ли затраты на брокера.
        # TODO: проверить сам order.
