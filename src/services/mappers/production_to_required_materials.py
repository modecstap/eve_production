from src.server.handlers.models.production_models import ProductionModel
from src.services.required_material.required_materials_payload import RequiredMaterialsPayload


class ProductionToRequiredMaterialsMapper:
    def __init__(self, model: ProductionModel):
        self._model = model

    def map(self) -> RequiredMaterialsPayload:
        return RequiredMaterialsPayload(
            product_type_id=self._model.type_id,
            count=self._model.count,
            blueprint_efficiency=self._model.blueprint_efficiency
        )
