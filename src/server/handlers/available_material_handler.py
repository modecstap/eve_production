from fastapi import HTTPException, status

from src.server.handlers.models import AvailableMaterialModel
from src.services.entity_service import TransactionService


class AvailableMaterialHandler:

    def __init__(self):
        self._service = TransactionService()

    @staticmethod
    def __raise_if_not_found(result, detail: str = "NOT_FOUND", status_code: int = status.HTTP_404_NOT_FOUND):
        if not result:
            raise HTTPException(status_code=status_code, detail=detail)

    async def get_all(self) -> list[AvailableMaterialModel]:
        models = await self._service.get_available_materials()
        self.__raise_if_not_found(models)
        return models
