from fastapi import HTTPException, status

from src.server.handlers.models.transactions_models import TransactionModel, InsertTransactionModel, \
    UpdateTransactionModel
from src.services.exceptions import NotFoundException
from src.services.utils import ServiceFactory


class TransactionHandler:

    def __init__(self):
        self._service = ServiceFactory.get_entity_service("transaction")

    @staticmethod
    def __raise_if_not_found(result, detail: str = "NOT_FOUND", status_code: int = status.HTTP_404_NOT_FOUND):
        if not result:
            raise HTTPException(status_code=status_code, detail=detail)

    @staticmethod
    def __raise_creation_error(result, detail="FAILED_CREATE", status_code=status.HTTP_400_BAD_REQUEST):
        if not result:
            raise HTTPException(status_code=status_code, detail=detail)

    async def get_all(
            self,
            replace_id_with_name: bool | None = None
    ) -> list[TransactionModel]:
        models = await self._service.get_models(replace_id_with_name)
        self.__raise_if_not_found(models)
        return models

    async def get(self, id: int) -> TransactionModel:
        try:
            models = await self._service.get_model_by_id(id)
            self.__raise_if_not_found(models)
            return models
        except NotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    async def create(self, data: InsertTransactionModel) -> TransactionModel:
        created_models = await self._service.add_models([data])
        self.__raise_creation_error(created_models)
        return created_models[0]

    async def create_bulk(self, data: list[InsertTransactionModel]) -> list[TransactionModel]:
        created_models = await self._service.add_models(data)
        self.__raise_creation_error(created_models)
        return created_models

    async def update(self, id: int, data: UpdateTransactionModel) -> TransactionModel:
        data.id = id
        updated_models = await self._service.update_models([data])
        self.__raise_if_not_found(updated_models)
        return updated_models[0]

    async def update_bulk(self, data: list[UpdateTransactionModel]) -> list[TransactionModel]:
        updated_models = await self._service.update_models(data)
        self.__raise_if_not_found(updated_models)
        return updated_models

    async def delete(self, id: int) -> dict:
        await self._service.delete_models([id])
        return {"message": "Deleted successfully", "status_code": status.HTTP_200_OK}

    async def get_available_materials(self):
        return await self._service.get_available_materials()
