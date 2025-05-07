from src.integration_tests.tests_api.base import PayloadBuilder
from src.integration_tests.tests_api.types.types_payload_builder import TypesPayloadBuilder


class MaterialListsPayloadBuilder(PayloadBuilder):
    async def build_payload(self) -> dict:
        types_payload = await TypesPayloadBuilder(self._client).build_payloads()
        response = await self._client.post("/api/types/bulk", json=types_payload)
        types = response.json()

        return {
            "material_id": types[0]["id"],
            "type_id": types[1]["id"],
            "count": "100"
        }

    async def build_payloads(self) -> list[dict]:
        types_payload = await TypesPayloadBuilder(self._client).build_payloads()
        response = await self._client.post("/api/types/bulk", json=types_payload)
        types: list[dict] = response.json()
        product_type = types.pop(0)["id"]

        return [
            {
                "material_id": type_,
                "type_id": product_type,
                "count": "100"
            } for type_ in types
        ]

    async def build_update_payload(self, id_: int) -> dict:
        response = await self._client.get(f"/api/material_lists/{id_}")
        material_list = response.json()
        return {
            "material_id": material_list["material_id"],
            "type_id": material_list["type_id"],
            "count": "1000"
        }

    async def build_update_payloads(self, ids_: list[int]) -> list[dict]:
        material_lists = []
        for id_ in ids_:
            response = await self._client.get(f"/api/material_lists/{id_}")
            material_lists.append(response.json())

        return [
            {
                "id": material_list["id"],
                "material_id": material_list["material_id"],
                "type_id": material_list["type_id"],
                "count": "1000"
            } for material_list in material_lists
        ]
