from typing import Type

from src.server.handlers.models.transactions_models import TransactionModel
from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import TransactionEntityMapper
from src.services.mappers.row_mappers import AvailableMaterialRowMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import TransactionRepository


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="transaction",
    )
)
class TransactionService(BaseEntityService):

    def __init__(
            self,
            repository: TransactionRepository=TransactionEntityMapper(),
            mapper: TransactionEntityMapper=TransactionEntityMapper(),
            available_material_mapper: AvailableMaterialRowMapper=AvailableMaterialRowMapper()
    ):
        super().__init__(repository, mapper)
        self._available_material_mapper = available_material_mapper

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
