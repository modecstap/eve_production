from typing import Type, TypeVar, cast

from src.server.handlers.models.material_list_models import MaterialListModel
from src.server.handlers.models.order_models import OrderModel
from src.server.handlers.models.product_models import ProductModel
from src.server.handlers.models.station_models import StationModel
from src.server.handlers.models.transactions_models import TransactionModel
from src.server.handlers.models.type_info_models import TypeInfoModel
from src.server.handlers.models.used_transactions import UsedTransactionModel
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.services.mappers.factory.mapper_config import MapperConfig
from src.storage.tables import MaterialList, Order, Product, Station, Transaction, TypeInfo, UsedTransactionList

T = TypeVar("T", bound=BaseEntityMapper)

class EntityMapperFactory:
    _classes: dict[str, tuple[Type[BaseEntityMapper], MapperConfig]] = {}
    _instances: dict[str, BaseEntityMapper] = {}
    _required: set[str] = {
        "material_list",
        "order",
        "product",
        "station",
        "transaction",
        "type_info",
        "used_transaction"
    }

    @classmethod
    def initialize(cls):
        cls.register(MapperConfig("material_list", MaterialListModel, MaterialList), BaseEntityMapper)
        cls.register(MapperConfig("order", OrderModel, Order), BaseEntityMapper)
        cls.register(MapperConfig("product", ProductModel, Product), BaseEntityMapper)
        cls.register(MapperConfig("station", StationModel, Station), BaseEntityMapper)
        cls.register(MapperConfig("transaction", TransactionModel, Transaction), BaseEntityMapper)
        cls.register(MapperConfig("type_info", TypeInfoModel, TypeInfo), BaseEntityMapper)
        cls.register(MapperConfig("used_transaction", UsedTransactionModel, UsedTransactionList), BaseEntityMapper)

    @classmethod
    def register(cls, configuration: MapperConfig, class_: Type[BaseEntityMapper]):
        cls._classes[configuration.name] = (class_, configuration)

    @classmethod
    def registration_decorator(cls, configuration: MapperConfig):
        def decorator(class_: Type[BaseEntityMapper]):
            EntityMapperFactory.register(configuration, class_)
            return class_

        return decorator

    @classmethod
    def get(cls, name: str) -> BaseEntityMapper:
        if name not in cls._classes:
            raise ValueError(f"'{name}' не зарегистрирован")

        if name not in cls._instances:
            class_, configuration = cls._classes[name]
            cls._instances[name] = class_(*configuration.unpack())

        return cls._instances[name]

    @classmethod
    def get_as(cls, name: str, expected_cls: Type[T]) -> T:
        repo = cls.get(name)
        if not isinstance(repo, expected_cls):
            raise TypeError(
                f"'{name}' должен быть экземпляром {expected_cls.__name__}, "
                f"но получен {type(repo).__name__}"
            )
        return cast(T, repo)

    @classmethod
    def validate_required(cls):
        missing = cls._required - cls._classes.keys()
        if missing:
            raise RuntimeError(f"Не зарегистрированы обязательные классы: {', '.join(sorted(missing))}")

    @classmethod
    def clear(cls):
        cls._classes.clear()
        cls._instances.clear()

    @classmethod
    def list_registered(cls) -> list[str]:
        return list(cls._classes.keys())
