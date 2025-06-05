from src.server.handlers.entity_handlers.entity_handler import EntityHandler
from src.server.handlers.models.station_models import StationModel, InsertStationModel, UpdateStationModel
from src.services.utils import ServiceFactory


class StationHandler(EntityHandler):
    MODEL = StationModel
    INSERT_MODEL = InsertStationModel
    UPDATE_MODEL = UpdateStationModel

    def __init__(self):
        super().__init__(ServiceFactory.get_service("station"))

    async def get_all(self) -> list[MODEL]:
        return await super().get_all()

    async def get(self, id: int) -> MODEL:
        return await super().get(id)

    async def create(self, data: INSERT_MODEL) -> MODEL:
        return await super().create(data)

    async def create_bulk(self, data: list[INSERT_MODEL]) -> list[MODEL]:
        return await super().create_bulk(data)

    async def update(self, id: int, data: UPDATE_MODEL) -> MODEL:
        return await super().update(id, data)

    async def update_bulk(self, data: list[UPDATE_MODEL]) -> list[MODEL]:
        return await super().update_bulk(data)

    async def delete(self, id: int) -> dict:
        return await super().delete(id)
