from abc import ABC

from src.services.mappers import BaseMapper


class BaseService(ABC):

    _main_mapper: BaseMapper

