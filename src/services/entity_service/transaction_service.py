from src.server.handlers.models import AvailableMaterialModel
from src.server.handlers.models.transactions_models import TransactionModel
from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers  import TransactionEntityMapper
from src.services.mappers.row_mappers import AvailableMaterialRowMapper
from src.storage.repositories import TransactionRepository


class TransactionService(BaseEntityService):

    def __init__(self):
        super().__init__()
        self._main_repository = TransactionRepository()
        self._main_mapper = TransactionEntityMapper()
        self._available_material_mapper = AvailableMaterialRowMapper()

    async def get_models(self, replace_id_with_name: bool) -> list[TransactionModel]:
        session = self._main_repository.create_session()
        try:
            entities = await self._main_repository.get_entities(
                session=session,
                replace_id_with_name=replace_id_with_name
            )
            models = self._main_mapper.entities_to_models(
                entities,
                replace_id_with_name=replace_id_with_name
            )
            return models
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


    async def get_available_materials(self) -> list[AvailableMaterialModel]:
        return await self.__try_get_available_materials()

    async def __try_get_available_materials(self):
        entities = await self._main_repository.get_available_materials()
        models = self._available_material_mapper.entities_to_models(entities)
        return models
