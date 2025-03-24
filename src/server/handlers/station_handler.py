from src.services.entity_service import StationService


class StationHandler:
    def __init__(self):
        self.station_service = StationService()

    async def get_stations(self):
        return await self.station_service.get_models()
