from fastapi import HTTPException, status
from pydantic import BaseModel

from src.services.available_material.available_material_model import AvailableMaterialModel
from src.services.utils import ServiceFactory


class AvailableMaterialHandler:

    def __init__(self):
        self._service = ServiceFactory.get_service("available_material")

    async def get_all(self) -> list[AvailableMaterialModel]:
        models = await self._service.do(None)
        return models
