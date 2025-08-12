from src.services.cost_calculator.production_facade_model import CostCalculatorFacadeModel
from src.services.required_material.required_materials_payload import RequiredMaterialsPayload


class ProductionToRequiredMaterialsMapper:

    def map(self, model: CostCalculatorFacadeModel) -> RequiredMaterialsPayload:
        return RequiredMaterialsPayload(
            product_type_id=model.type_id,
            count=model.count,
            blueprint_efficiency=model.blueprint_efficiency,
            station_id=model.station_id
        )
