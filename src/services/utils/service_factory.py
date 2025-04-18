from typing import Type

from src.services.base_service import BaseService
from src.services.utils import ServiceConfig


class ServiceFactory:
    _services: dict[str, BaseService] = {}

    @classmethod
    def register(cls, configuration: ServiceConfig, service: Type[BaseService]):
        cls._services[configuration.name] = service()

    @classmethod
    def service_registration_decorator(cls, configuration: ServiceConfig):
        def decorator(service_cls: Type[BaseService]):
            ServiceFactory.register(configuration, service_cls)
            return service_cls

        return decorator

    @classmethod
    def get_entity_service(cls, service_entity_name: str) -> BaseService:
        if service_entity_name not in cls._services:
            raise ValueError(f"Сервис типа '{service_entity_name}' не зарегистрирован")
        return cls._services[service_entity_name]
