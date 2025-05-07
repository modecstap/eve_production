from src.integration_tests.tests_api.base import BaseTestApi
from src.integration_tests.tests_api.material_lists.material_lists_payload_builder import MaterialListsPayloadBuilder


class TestMaterialLists(BaseTestApi):
    api_version = "api"
    endpoint = "materials_list"
    payload_builder = MaterialListsPayloadBuilder
