from fastapi import HTTPException, status

from src.server.handlers.models import AvailableMaterialModel
from src.server.handlers.models.transactions_models import TransactionModel, InsertTransactionModel, \
    UpdateTransactionModel
from src.services.entity_service import TransactionService
from src.services.exceptions import NotFoundException


class AvailableMaterialHandler:

    def __init__(self):
        self._service = TransactionService()

    @staticmethod
    def __raise_if_not_found(result, detail: str = "NOT_FOUND", status_code: int = status.HTTP_404_NOT_FOUND):
        if not result:
            raise HTTPException(status_code=status_code, detail=detail)

    async def get_all(self) -> AvailableMaterialModel:
        models = await self._service.get_available_materials()
        self.__raise_if_not_found(models)
        return models
