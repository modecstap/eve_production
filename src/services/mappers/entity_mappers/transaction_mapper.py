from src.server.handlers.models.transactions_models import TransactionModel
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.storage.tables import Transaction


class TransactionEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = TransactionModel
        self._entity_type = Transaction

    def entity_to_model(self, entity: Transaction, replace_id_with_name: bool = False ) -> TransactionModel:
        return TransactionModel(
            id=entity.id,
            release_date=entity.release_date,
            count=entity.count,
            material_id=entity.material.name if replace_id_with_name else entity.material_id,
            product_id=entity.product.name if replace_id_with_name and entity.product else entity.product_id,
            price=entity.price,
            remains=entity.remains
        )

    def entities_to_models(
            self,
            entities: list[Transaction],
            replace_id_with_name: bool = False
    ) -> list[TransactionModel]:
        return [self.entity_to_model(entity, replace_id_with_name) for entity in entities]

    def model_to_entity(self, model: TransactionModel) -> Transaction:
        return Transaction(
            id=getattr(model, 'id', None),
            release_date=model.release_date,
            count=model.count,
            material_id=getattr(model, "material_id", None),
            product_id=getattr(model, "product_id", None),
            price=model.price,
            remains=model.remains
        )
