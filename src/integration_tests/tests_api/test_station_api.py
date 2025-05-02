from src.integration_tests.tests_api.base import BaseTestApi
from src.server.handlers.models.station_models import StationModel
from src.storage.tables import Station


class TestStationApi(
    BaseTestApi
):
    api_version = "api"
    endpoint = "stations"
    model = StationModel
    entity = Station

    def build_valid_payload(self) -> dict:
        return {
            "name": "Station A",
            "material_efficiency": "0.15",
            "tax_percent": "3.5",
            "security_status": "0.8"
        }

    def build_invalid_payload(self) -> dict:
        return {
            "material_efficiency": "wrong",
            "tax_percent": "NaN",
            "security_status": -100
        }

    def update_payload(self, obj_id: int) -> dict:
        return {
            "id": obj_id,
            "name": "Updated Station",
            "material_efficiency": "0.25",
            "tax_percent": "7.5",
            "security_status": "0.95"
        }
