from src.server.handlers.models.station_models import StationModel, InsertStationModel, UpdateStationModel
from src.services.entity_service import StationService
from fastapi import HTTPException, status
from typing import List

from src.services.exceptions import NotFoundException


class StationHandler:
    def __init__(self):
        self._service = StationService()

    @staticmethod
    def __raise_if_not_found(result, detail: str = "NOT_FOUND", status_code: int = status.HTTP_404_NOT_FOUND):
        if not result:
            raise HTTPException(status_code=status_code, detail=detail)


    @staticmethod
    def __raise_creation_error(result, detail="FAILED_CREATE", status_code=status.HTTP_400_BAD_REQUEST):
        if not result:
            raise HTTPException(status_code=status_code, detail=detail)

    async def get_stations(self) -> List[StationModel]:
        stations = await self._service.get_models()
        self.__raise_if_not_found(stations)
        return stations

    async def get_station(self, station_id: int) -> StationModel:
        try:
            station = await self._service.get_model_by_id(station_id)
            self.__raise_if_not_found(station)
            return station
        except NotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    async def create_station(self, station_data: InsertStationModel) -> StationModel:
        created_station = await self._service.add_models([station_data])
        self.__raise_creation_error(created_station)
        return created_station[0]

    async def create_stations(self, stations_data: List[InsertStationModel]) -> List[StationModel]:
        created_stations = await self._service.add_models(stations_data)
        self.__raise_creation_error(created_stations)
        return created_stations

    async def update_station(self, station_id: int, station_data: UpdateStationModel) -> StationModel:
        station_data.id = station_id
        updated_station = await self._service.update_models([station_data])
        self.__raise_if_not_found(updated_station)
        return updated_station[0]

    async def update_stations(self, stations_data: List[UpdateStationModel]) -> List[StationModel]:
        updated_stations = await self._service.update_models(stations_data)
        self.__raise_if_not_found(updated_stations)
        return updated_stations

    async def delete_station(self, station_id: int) -> dict:
        await self._service.delete_models([station_id])
        return {"message": "Station deleted successfully", "status_code": status.HTTP_200_OK}
