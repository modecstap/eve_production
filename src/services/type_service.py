from src.services import BaseService
from src.services.mappers import TypeMapper
from src.storage.repositories import TypeInfoRepository


class TypeService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = TypeInfoRepository()
        self._main_mapper = TypeMapper()
