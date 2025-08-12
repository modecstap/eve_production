import pytest
from unittest.mock import AsyncMock, MagicMock

from src.services import ProductionService
from src.services.production.production_payload import ProductionPayload
from src.storage.tables import Product, Transaction


@pytest.fixture
def product_repo_mock():
    repo = MagicMock()
    repo.create_session = MagicMock(return_value=AsyncMock().__aenter__.return_value)
    repo.insert = AsyncMock()
    return repo

@pytest.fixture
def transaction_repo_mock():
    repo = MagicMock()
    repo.insert = AsyncMock()
    return repo

@pytest.fixture
def usage_repo_mock():
    repo = MagicMock()
    repo.register_usage = AsyncMock()
    return repo

@pytest.fixture
def service(product_repo_mock, transaction_repo_mock, usage_repo_mock):
    return ProductionService(
        product_repo=product_repo_mock,
        transaction_repo=transaction_repo_mock,
        product_usage_repo=usage_repo_mock
    )

@pytest.fixture
def payload():
    return ProductionPayload(
        station_id=1,
        blueprint_efficiency=0.9,
        release_date="2025-08-12",
        product_type_id=100,
        count=5,
        assembly_cost=200
    )


# ---------- Позитивные тесты ----------

@pytest.mark.asyncio
async def test_do_inserts_product_and_transaction(service, product_repo_mock, transaction_repo_mock, usage_repo_mock, payload):
    await service.do(payload)

    # Проверяем вставку продукта
    product_repo_mock.insert.assert_awaited_once()
    inserted_product = product_repo_mock.insert.await_args.args[0][0]
    assert isinstance(inserted_product, Product)
    assert inserted_product.station_id == payload.station_id
    assert inserted_product.blueprint_efficiency == payload.blueprint_efficiency

    # Проверяем вставку транзакции
    transaction_repo_mock.insert.assert_awaited_once()
    inserted_transaction = transaction_repo_mock.insert.await_args.args[0][0]
    assert isinstance(inserted_transaction, Transaction)
    assert inserted_transaction.count == payload.count
    assert inserted_transaction.price == payload.assembly_cost

    # Проверяем регистрацию использования материалов
    usage_repo_mock.register_usage.assert_awaited_once()


@pytest.mark.asyncio
async def test_do_commits_session(service, product_repo_mock, payload):
    mock_session = AsyncMock()
    product_repo_mock.create_session.return_value.__aenter__.return_value = mock_session

    await service.do(payload)
    mock_session.commit.assert_awaited_once()


# ---------- Негативные тесты ----------

@pytest.mark.asyncio
async def test_do_fails_on_product_insert_error(service, product_repo_mock, payload):
    product_repo_mock.insert.side_effect = Exception("DB insert error")

    with pytest.raises(Exception) as exc_info:
        await service.do(payload)

    assert "DB insert error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_do_fails_on_transaction_insert_error(service, transaction_repo_mock, payload):
    transaction_repo_mock.insert.side_effect = Exception("Transaction error")

    with pytest.raises(Exception) as exc_info:
        await service.do(payload)

    assert "Transaction error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_do_fails_on_usage_registration_error(service, usage_repo_mock, payload):
    usage_repo_mock.register_usage.side_effect = Exception("Usage error")

    with pytest.raises(Exception) as exc_info:
        await service.do(payload)

    assert "Usage error" in str(exc_info.value)
