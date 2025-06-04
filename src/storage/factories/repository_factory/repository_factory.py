from typing import Type

from src.storage.factories.repository_factory.repository_config import RepositoryConfig
from src.storage.repositories import BaseRepository, TransactionRepository
from src.storage.tables import MaterialList, Order, Product, Station, Transaction, TypeInfo, UsedTransactionList


class RepositoryFactory:
    _repository_classes: dict[str, tuple[Type[BaseRepository], Any]] = {}
    _instances: dict[str, BaseRepository] = {}
    _required: set[str] = {
        "material_list_repository",
        "order_repository",
        "product_repository",
        "station_repository",
        "transaction_repository",
        "type_info_repository",
        "used_transaction_repository"
    }

    @classmethod
    def initialize(cls):
        cls.register(RepositoryConfig("material_list_repository", MaterialList), BaseRepository)
        cls.register(RepositoryConfig("order_repository", Order), BaseRepository)
        cls.register(RepositoryConfig("product_repository", Product), BaseRepository)
        cls.register(RepositoryConfig("station_repository", Station), BaseRepository)
        cls.register(RepositoryConfig("transaction_repository", Transaction), TransactionRepository)
        cls.register(RepositoryConfig("type_info_repository", TypeInfo), BaseRepository)
        cls.register(RepositoryConfig("used_transaction_repository", UsedTransactionList), BaseRepository)

    @classmethod
    def register(cls, configuration: RepositoryConfig, repository_cls: Type[BaseRepository]):
        cls._repository_classes[configuration.name] = (repository_cls, configuration.entity)

    @classmethod
    def repository_registration_decorator(cls, configuration: RepositoryConfig):
        def decorator(repository_cls: Type[BaseRepository]):
            RepositoryFactory.register(configuration, repository_cls)
            return repository_cls
        return decorator

    @classmethod
    def get_entity_repository(cls, repository_entity_name: str) -> BaseRepository:
        if repository_entity_name not in cls._repository_classes:
            raise ValueError(f"Репозиторий '{repository_entity_name}' не зарегистрирован")

        if repository_entity_name not in cls._instances:
            repository_cls, entity = cls._repository_classes[repository_entity_name]
            cls._instances[repository_entity_name] = repository_cls(entity)

        return cls._instances[repository_entity_name]

    @classmethod
    def validate_required(cls):
        missing = cls._required-cls._repository_classes.keys()
        if missing:
            raise RuntimeError(f"Не зарегистрированы обязательные репозитории: {', '.join(sorted(missing))}")

    @classmethod
    def clear(cls):
        cls._repository_classes.clear()
        cls._instances.clear()

    @classmethod
    def list_registered(cls) -> list[str]:
        return list(cls._repository_classes.keys())