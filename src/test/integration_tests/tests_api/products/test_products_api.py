from src.test.integration_tests.tests_api.base import BaseTestApi
from src.test.integration_tests.tests_api.products.product_payload_builder import ProductPayloadBuilder


class TestProductsApi(BaseTestApi):
    api_version = "api"
    endpoint = "products"
    payload_builder = ProductPayloadBuilder
