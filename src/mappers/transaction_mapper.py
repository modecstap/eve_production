from src.mappers import BaseMapper
from src.server.handlers.models import TransactionModel
from src.server.handlers.models.available_materials_model import AvailableMaterialModel
from src.storage.tables import Transaction


class TransactionMapper(BaseMapper):
    def __init__(self):
        super().__init__()
        self._model_type = TransactionModel
        self._entity_type = Transaction

    def available_material_entity_to_model(self, entity) -> AvailableMaterialModel:
        return AvailableMaterialModel(
            name=entity.name,
            count=entity.count,
            mean_price=entity.mean_price
        )

    def available_material_entities_to_models(self, entities) -> list[AvailableMaterialModel]:
        return [self.available_material_entity_to_model(entity) for entity in entities]
