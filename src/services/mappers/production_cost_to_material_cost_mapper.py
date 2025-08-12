from src.services import CostCalculatorFacadeModel
from src.services.production_cost_calculator.production_cost_payload import ProductionCostPayload


class ProductionCostToMaterialCostMapper:

    async def map(self, input_model: ProductionCostPayload) -> CostCalculatorFacadeModel:
        return CostCalculatorFacadeModel(
            type_id=input_model.type_id,
            release_date=input_model.release_date,
            count=input_model.count,
            station_id=input_model.station_id,
            blueprint_efficiency=input_model.blueprint_efficiency
        )
