from src.integration_tests.tests_api.base import BaseTestApi
from src.integration_tests.tests_api.material_lists.material_lists_payload_builder import MaterialListsPayloadBuilder


class TestMaterialLists(BaseTestApi):
    api_version = "api"
    endpoint = "material_lists"
    payload_builder = MaterialListsPayloadBuilder
