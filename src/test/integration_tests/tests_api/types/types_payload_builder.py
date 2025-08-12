from src.test.integration_tests.tests_api.base import PayloadBuilder


class TypesPayloadBuilder(PayloadBuilder):

    async def build_payload(self) -> dict:
        return {
            "name": "Test type",
            "is_produced": False
        }

    async def build_payloads(self) -> list[dict]:
        return [
            {
                "name": "Test type A",
                "is_produced": True
            },
            {
                "name": "Test type B",
                "is_produced": True
            },
            {
                "name": "Test type C",
                "is_produced": True
            }
        ]

    async def build_update_payload(self, id_: int) -> dict:
        return {
            "id": id_,
            "name": "updated type",
            "is_produced": True
        }

    async def build_update_payloads(self, ids_: list[int]) -> list[dict]:
        return [
            {
                "id": id_,
                "name": "updated type A",
                "is_produced": False
            } for id_ in ids_
        ]
