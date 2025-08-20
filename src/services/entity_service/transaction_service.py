from src.server.handlers.models.transactions_models import TransactionModel
from src.services.entity_service import BaseEntityService
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.services.mappers.transaction_name_mapper import TransactionNameMapper
from src.services.utils import ServiceFactory, ServiceConfig
from src.storage.repositories import BaseRepository
from src.storage.tables import Transaction


@ServiceFactory.service_registration_decorator(
    ServiceConfig(
        name="transaction",
    )
)
class TransactionService(BaseEntityService):

    def __init__(
            self,
            repository: BaseRepository = BaseRepository(Transaction),
            mapper: BaseEntityMapper = BaseEntityMapper(TransactionModel, Transaction),
    ):
        super().__init__(repository, mapper)

    async def get_models(self, replace_id_with_name: bool) -> list[TransactionModel]:
        session = self._main_repository.create_session()
        try:
            entities = await self._main_repository.get_entities(
                session=session
            )
            if replace_id_with_name:
                return TransactionNameMapper.entities_to_models(
                    entities
                )

            return self._main_mapper.entities_to_models(
                entities,
            )
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
