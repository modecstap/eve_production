from src.server.handlers.models.transactions_models import TransactionModel
from src.services.mappers.entity_mappers import BaseEntityMapper
from src.storage.tables import Transaction


class TransactionEntityMapper(BaseEntityMapper):
    def __init__(self):
        super().__init__()
        self._model_type = TransactionModel
        self._entity_type = Transaction

    def entity_to_model(self, entity: Transaction, replace_id_with_name: bool) -> TransactionModel:
        return TransactionModel(
            id=entity.id,
            release_date=entity.release_date,
            count=entity.count,
            material=entity.material.name if replace_id_with_name else entity.material_id,
            product=entity.product.name if replace_id_with_name and entity.product else entity.product_id,
            price=entity.price,
            remains=entity.remains
        )

    def entities_to_models(self, entities: list[Transaction], replace_id_with_name: bool) -> list[Transaction]:
        return [self.entity_to_model(entity, replace_id_with_name) for entity in entities]
    def model_to_entity(self, model: TransactionModel) -> Transaction:
        return Transaction(
            id=model.id,
            release_date=model.release_date,
            count=model.count,
            material_id=model.material if isinstance(model.material, int) else None,
            product_id=model.product if isinstance(model.product, int) else None,
            price=model.price,
            remains=model.remains
        )
