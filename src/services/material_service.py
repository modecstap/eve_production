from src.mappers import MaterialMapper
from src.services import BaseService
from src.storage.repositories import MaterialRepository


class MaterialService(BaseService):

    def __init__(self):
        super().__init__()
        self._main_repository = MaterialRepository()
        self._main_mapper = MaterialMapper()
