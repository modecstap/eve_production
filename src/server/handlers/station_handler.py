from src.services.enetity_serice import StationService


class StationHandler:
    def __init__(self):
        self.station_service = StationService()

    async def get_stations(self):
        return await self.station_service.get_models()
