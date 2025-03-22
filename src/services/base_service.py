from abc import ABC

from src.services.mappers.entity_mappers import BaseMapper


class BaseService(ABC):

    _main_mapper: BaseMapper

