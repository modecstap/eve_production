from typing import Type

from src.services.entity_service import BaseEntityService
from src.services.utils import ServiceConfig


class EntityServiceFactory:
    _services: dict[str, BaseEntityService] = {}

    @classmethod
    def register(cls, configuration: ServiceConfig, service: Type[BaseEntityService]):
        cls._services[configuration.name] = service(
            repository=configuration.repository,
            mapper=configuration.mapper
        )

    @classmethod
    def service_registration_decorator(cls, configuration: ServiceConfig):
        def decorator(service_cls: Type[BaseEntityService]):
            EntityServiceFactory.register(configuration, service_cls)
            return service_cls

        return decorator

    @classmethod
    def get_entity_service(cls, service_entity_name: str) -> BaseEntityService:
        if service_entity_name not in cls._services:
            raise ValueError(f"Сервис типа '{service_entity_name}' не зарегистрирован")
        return cls._services[service_entity_name]
