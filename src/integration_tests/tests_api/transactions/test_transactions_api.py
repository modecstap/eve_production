from src.integration_tests.tests_api.base import BaseTestApi
from src.integration_tests.tests_api.stations.stations_payload_builder import StationsPayloadBuilder
from src.integration_tests.tests_api.transactions.transactions_payload_builder import TransactionsPayloadBuilder


class TestTransactionSApi(
    BaseTestApi
):
    api_version = "api"
    endpoint = "transactions"
    payload_builder = TransactionsPayloadBuilder
