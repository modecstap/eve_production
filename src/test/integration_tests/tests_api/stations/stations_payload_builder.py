from src.test.integration_tests.tests_api.base import PayloadBuilder


class StationsPayloadBuilder(PayloadBuilder):

    async def build_payload(self) -> dict:
        return {
            "name": "Test station",
            "material_efficiency": "1",
            "tax_percent": "0.05",
            "security_status": "0.8"
        }

    async def build_payloads(self) -> list[dict]:
        return [
            {
                "name": "Test station A",
                "material_efficiency": "1",
                "tax_percent": "0.05",
                "security_status": "0.7"
            },
            {
                "name": "Test station B",
                "material_efficiency": "0.9",
                "tax_percent": "0.056",
                "security_status": "0.8"
            },
            {
                "name": "Test station C",
                "material_efficiency": "0.8",
                "tax_percent": "0.057",
                "security_status": "0.6"
            }
        ]

    async def build_update_payload(self, id_) -> dict:
        return {
            "id": id_,
            "name": "updated station",
            "material_efficiency": "0.9",
            "tax_percent": "0.056",
            "security_status": "0.8"
        }

    async def build_update_payloads(self, ids_) -> list[dict]:
        return [
            {
                "id": id_,
                "name": "updated station A",
                "material_efficiency": "0.9",
                "tax_percent": "0.056",
                "security_status": "0.8"
            } for id_ in ids_
        ]
