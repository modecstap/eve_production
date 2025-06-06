from src.server.handlers.models.transactions_models import TransactionModel
from src.storage.tables import Transaction


class TransactionNameMapper:
    """
    Данный маппер требует держать открытой сессию, породившую entity
    """

    def entity_to_model(self, entity: Transaction) -> TransactionModel:
        return TransactionModel(
            id=entity.id,
            release_date=entity.release_date,
            count=entity.count,
            material_id=entity.material.name,
            product_id=entity.product.name,
            price=entity.price,
            remains=entity.remains
        )

    def entities_to_models(self, entities: list[Transaction]) -> list[TransactionModel]:
        return [self.entity_to_model(entity) for entity in entities]
