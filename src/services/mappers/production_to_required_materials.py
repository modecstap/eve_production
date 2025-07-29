from src.services.cost_calculator.production_facade_model import CostCalculatorFacadeModel
from src.services.required_material.required_materials_payload import RequiredMaterialsPayload


class ProductionToRequiredMaterialsMapper:
    def __init__(self, model: CostCalculatorFacadeModel):
        self._model = model

    def map(self) -> RequiredMaterialsPayload:
        return RequiredMaterialsPayload(
            product_type_id=self._model.type_id,
            count=self._model.count,
            blueprint_efficiency=self._model.blueprint_efficiency
        )
