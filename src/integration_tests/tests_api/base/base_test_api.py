from abc import ABC

import pytest

from src.integration_tests.tests_api.base import TestApiInfrastructure, TestPost, TestGet, TestPut, TestDelete


class BaseTestApi(
    TestApiInfrastructure,
    TestGet,
    TestPost,
    TestPut,
    TestDelete,
    ABC
):
    api_version: str
    endpoint: str

    @pytest.mark.asyncio
    async def test_post_single(self):
        # Arrange
        payload = self.build_valid_payload()

        # Act
        response = await self.client.post(f"/{self.api_version}/{self.endpoint}/", json=payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        self.assert_equal(data, payload)

    @pytest.mark.asyncio
    async def test_post_multiple(self):
        # Arrange
        payloads = [self.build_valid_payload() for _ in range(3)]

        # Act
        response = await self.client.post(f"/{self.api_version}/{self.endpoint}/bulk", json=payloads)

        # Assert
        assert response.status_code == 200
        returned = response.json()
        assert len(returned) == 3
        for actual, expected in zip(returned, payloads):
            self.assert_equal(actual, expected)

    @pytest.mark.asyncio
    async def test_get_single(self):
        # Arrange
        payload = self.build_valid_payload()
        post_response = await self.client.post(f"/{self.api_version}/{self.endpoint}/", json=payload)
        obj_id = post_response.json()["id"]

        # Act
        get_response = await self.client.get(f"/{self.api_version}/{self.endpoint}/{obj_id}")

        # Assert
        assert get_response.status_code == 200
        self.assert_equal(get_response.json(), {**payload, "id": obj_id})

    @pytest.mark.asyncio
    async def test_get_multiple(self):
        # Arrange
        payloads = [self.build_valid_payload() for _ in range(2)]
        post_response = await self.client.post(f"/{self.api_version}/{self.endpoint}/bulk", json=payloads)
        ids = [item["id"] for item in post_response.json()]

        # Act
        get_response = await self.client.get(f"/{self.api_version}/{self.endpoint}/",
                                             params={"ids": ",".join(map(str, ids))})

        # Assert
        assert get_response.status_code == 200
        returned = get_response.json()
        for actual, expected in zip(returned, payloads):
            del actual["id"]
            self.assert_equal(actual, expected)

    @pytest.mark.asyncio
    async def test_put_single(self):
        # Arrange
        payload = self.build_valid_payload()
        post_response = await self.client.post(f"/{self.api_version}/{self.endpoint}/", json=payload)
        obj_id = post_response.json()["id"]
        update = self.update_payload(obj_id)

        # Act
        put_response = await self.client.put(f"/{self.api_version}/{self.endpoint}/{obj_id}", json=update)

        # Assert
        assert put_response.status_code == 200
        self.assert_equal(put_response.json(), {**update, "id": obj_id})

    @pytest.mark.asyncio
    async def test_put_multiple(self):
        # Arrange
        payloads = [self.build_valid_payload() for _ in range(2)]
        post_response = await self.client.post(f"/{self.api_version}/{self.endpoint}/bulk", json=payloads)
        items = post_response.json()
        updated = [self.update_payload(item["id"]) for item in items]

        # Act
        put_response = await self.client.put(f"/{self.api_version}/{self.endpoint}/", json=updated)

        # Assert
        assert put_response.status_code == 200
        returned = put_response.json()
        for actual, expected in zip(returned, updated):
            self.assert_equal(actual, expected)

    @pytest.mark.asyncio
    async def test_delete_single(self):
        # Arrange
        payload = self.build_valid_payload()
        post_response = await self.client.post(f"/{self.api_version}/{self.endpoint}/", json=payload)
        obj_id = post_response.json()["id"]

        # Act
        del_response = await self.client.delete(f"/{self.api_version}/{self.endpoint}/{obj_id}")

        # Assert
        assert del_response.status_code == 200
        get_response = await self.client.get(f"/{self.api_version}/{self.endpoint}/{obj_id}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_multiple(self):
        # Arrange
        payloads = [self.build_valid_payload() for _ in range(2)]
        post_response = await self.client.post(f"/{self.api_version}/{self.endpoint}/bulk", json=payloads)
        ids = [item["id"] for item in post_response.json()]

        # Act
        del_response = await self.client.request("DELETE", f"/{self.api_version}/{self.endpoint}/bulk",
                                                 json={"ids": ids})

        # Assert
        assert del_response.status_code == 200
        for obj_id in ids:
            get_response = await self.client.get(f"/{self.api_version}/{self.endpoint}/{obj_id}")
            assert get_response.status_code == 404
