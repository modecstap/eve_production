from src.test.integration_tests.tests_api.base import BaseTestApi
from src.test.integration_tests.tests_api.types.types_payload_builder import TypesPayloadBuilder


class TestTypesApi(
    BaseTestApi
):
    api_version = "api"
    endpoint = "types"
    payload_builder = TypesPayloadBuilder
