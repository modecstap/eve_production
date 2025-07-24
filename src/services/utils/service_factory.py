from typing import Type

from src.services.AService import Service
from src.services.utils import ServiceConfig


class ServiceFactory:
    _services: dict[str, Service] = {}

    @classmethod
    def register(cls, configuration: ServiceConfig, service: Type[Service]):
        cls._services[configuration.name] = service()

    @classmethod
    def service_registration_decorator(cls, configuration: ServiceConfig):
        def decorator(service_cls: Type[Service]):
            ServiceFactory.register(configuration, service_cls)
            return service_cls

        return decorator

    @classmethod
    def get_service(cls, service_entity_name: str) -> Service:
        if service_entity_name not in cls._services:
            raise ValueError(f"Сервис типа '{service_entity_name}' не зарегистрирован")
        return cls._services[service_entity_name]
