from aiohttp.web import Request

from src.services import StationService


class StationHandler:
    def __init__(self):
        self.station_service = StationService()

    async def get_stations(self, request: Request):
        return await self.station_service.get_models()
