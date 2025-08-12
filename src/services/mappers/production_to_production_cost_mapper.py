from src.services.production.production_payload import ProductionPayload
from src.services.production_cost_calculator.production_cost_payload import ProductionCostPayload


class ProductionToProductionCostMapper:

    async def map(self, input_model: ProductionPayload) -> ProductionCostPayload:
        return ProductionCostPayload(
            production_cost=input_model.assembly_cost,
            type_id=input_model.product_type_id,
            release_date=input_model.release_date,
            count=input_model.count,
            station_id=input_model.station_id,
            blueprint_efficiency=input_model.blueprint_efficiency
        )
