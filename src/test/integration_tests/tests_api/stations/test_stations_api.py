from src.test.integration_tests.tests_api.base import BaseTestApi
from src.test.integration_tests.tests_api.stations.stations_payload_builder import StationsPayloadBuilder


class TestStationSApi(
    BaseTestApi
):
    api_version = "api"
    endpoint = "stations"
    payload_builder = StationsPayloadBuilder
